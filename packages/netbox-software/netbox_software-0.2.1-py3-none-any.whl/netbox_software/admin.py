from django.contrib import admin
from .models import DeviceSoftware, Vendor, SoftwareType


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(SoftwareType)
class SoftwareTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(DeviceSoftware)
class DeviceSoftwareAdmin(admin.ModelAdmin):
    list_display = ('name', 'software_type', 'vendor', 'version')

