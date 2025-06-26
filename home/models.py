from django.db import models
from uuid import uuid4
from home.models import *
from django.db.models import Sum

class Project(models.Model):
    project_name = models.CharField(max_length=200, null=True, blank=True)
    # created_date = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name
    
class Platform(models.Model):
    platform_name = models.CharField(max_length=200, null=True, blank=True)
    # created_date = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.platform_name

# class Plot(models.Model):
#     project       = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
#     plot_no       = models.CharField(max_length=200, null=True, blank=True)
#     created_date  = models.DateTimeField(auto_now_add=True)
#     updated_date  = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.plot_no


class Record(models.Model):
    team_leader_name   = models.CharField(max_length=200, null=True, blank=True)
    associate_name  = models.CharField(max_length=200, null=True, blank=True)
    mobile  = models.CharField(max_length=13)
    project   = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    platform   = models.ForeignKey(Platform, on_delete=models.CASCADE, null=True, blank=True)
    username   = models.CharField(max_length=200, null=True, blank=True)
    password   = models.CharField(max_length=200, null=True, blank=True)
    total_price = models.IntegerField(null=True, blank=True)
    sum_amount  = models.IntegerField(null=True, blank=True)
    leads  = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
# class Payment(models.Model):
#     records = models.ForeignKey(Record, on_delete=models.CASCADE, null=True, blank=True)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
#     platform = models.ForeignKey(Platform, on_delete=models.CASCADE, null=True, blank=True)
#     # project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
#     # platform = models.ForeignKey(Platform, on_delete=models.CASCADE, null=True, blank=True)
#     payment_type = models.CharField(max_length=10, null=True, blank=True)
#     total_price = models.IntegerField(null=True, blank=True)
#     received_amount = models.IntegerField(null=True, blank=True)
#     total_amount = models.IntegerField(null=True, blank=True)
#     leads = models.CharField(max_length=200, null=True, blank=True)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)
#     def __str__(self):
#         return self.total_amount

class Payment(models.Model):
    records = models.ForeignKey(Record, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, null=True, blank=True)
    payment_type = models.CharField(max_length=10, null=True, blank=True)
    total_price = models.IntegerField(null=True, blank=True)
    received_amount = models.IntegerField(null=True, blank=True)
    total_amount = models.IntegerField(null=True, blank=True)
    leads = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.total_amount)
    
