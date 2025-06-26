from django.contrib import admin
from .models import *

from django.contrib import admin
from .models import Project, Record, Platform


class RecordUser(admin.ModelAdmin):
    list_display = ['team_leader_name','associate_name','mobile','project','platform', 'username', 'password', 'total_price', 'sum_amount', 'leads', 'start_date','end_date']


class ProjectUser(admin.ModelAdmin):
    list_display = ['project_name']


class PlatformUser(admin.ModelAdmin):
    list_display = ['platform_name']



admin.site.register(Project, ProjectUser)
admin.site.register(Platform, PlatformUser)

admin.site.register(Record, RecordUser)
admin.site.register(Payment)



