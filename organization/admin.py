from django.contrib import admin
from .models import Organization, Lead, Campaign
# Register your models here.


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'address')


class LeadAdmin(admin.ModelAdmin):
    list_display = ('lead_name', 'address')


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('campaign_name', 'organization')

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Lead, LeadAdmin)
admin.site.register(Campaign, CampaignAdmin)
