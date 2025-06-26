from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.log_in, name='log_in'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-record/<int:id>/', views.edit_record, name='edit_record'),
    path('update-record/', views.update_record, name='update_record'),
    path('payment_details/<int:id>/', views.payment_details, name='payment_details'),
    path('export/', views.export_users, name='export_users'),
    path('get-team-leader-name/', views.get_team_leader_name, name='get_team_leader_name'),
]
