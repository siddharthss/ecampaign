from django.contrib import admin
from .models import Organization
# Register your models here.


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'address')

admin.site.register(Organization, OrganizationAdmin)
