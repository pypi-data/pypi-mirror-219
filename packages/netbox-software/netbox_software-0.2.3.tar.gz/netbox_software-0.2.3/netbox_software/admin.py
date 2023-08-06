from django.contrib import admin
from .models import DeviceSoftware, Vendor, SoftwareType, ApplicationVersion, Application


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(SoftwareType)
class SoftwareTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'software_type', 'vendor')


@admin.register(ApplicationVersion)
class ApplicationVersionAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(DeviceSoftware)
class DeviceSoftwareAdmin(admin.ModelAdmin):
    list_display = ('app', 'assigned_object', 'version')
