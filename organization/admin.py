from django.contrib import admin
from .models import Organization, Lead, Campaign, ScheduleLog,Rule
# Register your models here.


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')


class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'organization')


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization')


class ScheduleLogAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'send_at')


class RuleAdmin(admin.ModelAdmin):
    list_display = ('source', 'value', 'operator')

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Lead, LeadAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(ScheduleLog, ScheduleLogAdmin)
admin.site.register(Rule, RuleAdmin)
