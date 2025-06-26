from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Record, Project, Payment, Platform
from django.db import IntegrityError
from datetime import datetime, timedelta
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
import pandas as pd
from datetime import datetime
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.db import transaction
import json
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


def log_in(request):
     if request.method == "GET":
         return render(request, 'log_in.html')
     if request.method == "POST":
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Email/Username or Password Incorrect")
            return redirect('log_in')
        if user is not None:
            messages.success(request, "User login successfully")
            return redirect('index')
        # return render(request, 'index.html')
        
def logout_view(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('log_in')
    # return render(request, 'log_in.html')

def edit_record(request, id):
    record = get_object_or_404(Record, id=id)
    data = {
        'id': record.id,
        'team_leader_name': record.team_leader_name,
        'associate_name': record.associate_name,
        'mobile': record.mobile,
        'project': record.project.id if record.project else '',
        'platform': record.platform.id if record.platform else '',
        'username': record.username,
        'password': record.password,
        'total_price': record.total_price,
        'sum_amount': record.sum_amount,
        'leads': record.leads,
        'start_date': record.start_date,
        'end_date': record.end_date
    }
    return JsonResponse(data)


@require_POST
def update_record(request):
    try:
        data = json.loads(request.body)

        record_id = data.get('id')
        project_id = data.get('project')
        platform_id = data.get('platform')
        
        if not record_id or not project_id or not platform_id:
            return JsonResponse({'message': 'Missing required fields'}, status=400)

        leads = data.get('leads', 0)
        total_price = data.get('total_price', 0)
        sum_amount = data.get('sum_amount', 0)
        received_amount = data.get('received_amount', 0)
        start_date = data.get('start_date', '')
        end_date = data.get('end_date', '')

        try:
            total_price = float(total_price)
            sum_amount = float(sum_amount)
        except ValueError:
            return JsonResponse({'message': 'Invalid data format for total_price or sum_amount'}, status=400)
        
        total_received_amount = sum_amount + total_price

        with transaction.atomic():
            record = get_object_or_404(Record, id=record_id)
            project = get_object_or_404(Project, id=project_id)
            platform = get_object_or_404(Platform, id=platform_id)

            record.project = project
            record.platform = platform
            record.sum_amount = total_received_amount
            record.total_price = total_price
            record.leads = leads
            record.start_date = start_date
            record.end_date = end_date
            record.save()

            Payment.objects.create(
                records=record,
                project=project,
                platform=platform,
                total_amount=total_price,
                received_amount=total_received_amount,
                leads=leads,
                start_date=start_date,
                end_date=end_date,
            )

        return JsonResponse({'message': 'Record updated successfully', 'status': '200', 'total_price': total_price})
    
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


def payment_details(request, id):
    myrecord = Record.objects.filter(id=id).last()
    payment = Payment.objects.filter(records=myrecord.id).order_by('-created_date')
    return render(request, 'payment_details.html', {'payment': payment})

# @login_required(login_url='log_in')
def index(request):
    users = Record.objects.all()
    
    if request.method == 'POST':
        team_leader_name = request.POST.get('team_leader_name')
        associate_name = request.POST.get('associate_name')
        mobile = request.POST.get('mobile')
        project_id = request.POST.get('project')
        platform_id = request.POST.get('platform')
        username = request.POST.get('username')
        password = request.POST.get('password')
        total_price = request.POST.get('total_price')
        sum_amount = request.POST.get('sum_amount')
        leads = request.POST.get('leads')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('index')

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return redirect('index')

        try:
            platform = Platform.objects.get(id=platform_id)
        except Platform.DoesNotExist:
            messages.error(request, "Selected platform does not exist.")
            return redirect('index')
        
        if Record.objects.filter(mobile=mobile).exists():
            messages.error(request, "A customer with this mobile number already exists.")
        else:
            try:
                myrecord = Record.objects.create(
                    team_leader_name=team_leader_name,
                    associate_name=associate_name,
                    mobile=mobile,
                    project=project,
                    platform=platform,
                    username=username,
                    password=password,
                    total_price=total_price,
                    sum_amount=sum_amount,
                    leads=leads,
                    start_date=start_date,
                    end_date=end_date,
                    
                )
                payment = Payment.objects.create(
                    records=myrecord,
                    project=project,
                    platform=platform,
                    total_amount=total_price,
                    leads=leads,
                    start_date=start_date,
                    end_date=end_date,
                    received_amount=sum_amount
                )

                messages.success(request, "Customer Created Successfully.")
                return redirect('index')
            except IntegrityError as e:
                messages.error(request, f"An error occurred while creating the customer: {e}. Please try again.")

    projects = Project.objects.all()
    platforms = Platform.objects.all()
    
    context = {
        # 'users': users,
        'users': users,
        'projects': projects,
        'platforms':platforms,
        'messages': messages.get_messages(request),
    }
    return render(request, 'index.html', context)

def export_users(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        if selected_ids:
            users = Record.objects.filter(id__in=selected_ids).values(
                'team_leader_name', 'associate_name', 'mobile', 'project__project_name', 'platform__platform_name', 
                'username', 'password', 'sum_amount',  
                'leads', 'start_date', 'end_date', 'created_date'
            )
        else:
            users = Record.objects.all().values(
                'team_leader_name', 'associate_name', 'mobile', 'project__project_name', 'platform__platform_name', 
                'username', 'password', 'sum_amount', 'leads', 
                'start_date', 'end_date', 'created_date'
            )
        df = pd.DataFrame(list(users))

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'

        df.to_csv(path_or_buf=response, index=False)

        return response
    else:
        return HttpResponse("Invalid request method.")

def get_team_leader_name(request):
    associate_name = request.GET.get('associate_name')
    try:
        record = Record.objects.get(associate_name=associate_name)
        team_leader_name = record.team_leader_name
        return JsonResponse({'team_leader_name': team_leader_name})
    except Record.DoesNotExist:
        return JsonResponse({'error': 'Associate not found'}, status=404)