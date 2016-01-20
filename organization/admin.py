from django.contrib import admin
from .models import Organization, Lead, Campaign, ScheduleLog
# Register your models here.


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'address')


class LeadAdmin(admin.ModelAdmin):
    list_display = ('lead_name', 'address', 'organization')


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('campaign_name', 'organization')


class ScheduleLogAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'send_at')

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Lead, LeadAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(ScheduleLog, ScheduleLogAdmin)
