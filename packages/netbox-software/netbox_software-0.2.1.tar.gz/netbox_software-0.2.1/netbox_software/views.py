from django.contrib.auth.mixins import PermissionRequiredMixin
from netbox.views import generic
from . import forms, models, tables, filtersets


### Vendor
class VendorView(PermissionRequiredMixin, generic.ObjectView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = models.Vendor.objects.all()


class VendorListView(PermissionRequiredMixin, generic.ObjectListView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = models.Vendor.objects.all()
    table = tables.VendorTable
    filterset = filtersets.VendorFilterSet
    filterset_form = forms.VendorFilterForm


class VendorEditView(PermissionRequiredMixin, generic.ObjectEditView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = models.Vendor.objects.all()
    form = forms.VendorForm

    template_name = 'netbox_software/vendor_edit.html'


class VendorDeleteView(PermissionRequiredMixin, generic.ObjectDeleteView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = models.Vendor.objects.all()


### SoftwareType
class SoftwareTypeView(PermissionRequiredMixin, generic.ObjectView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = models.SoftwareType.objects.all()


class SoftwareTypeListView(PermissionRequiredMixin, generic.ObjectListView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = models.SoftwareType.objects.all()
    table = tables.SoftwareTypeTable
    filterset = filtersets.SoftwareTypeFilterSet
    filterset_form = forms.SoftwareTypeFilterForm


class SoftwareTypeEditView(PermissionRequiredMixin, generic.ObjectEditView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = models.SoftwareType.objects.all()
    form = forms.SoftwareTypeForm

    template_name = 'netbox_software/softwaretype_edit.html'


class SoftwareTypeDeleteView(PermissionRequiredMixin, generic.ObjectDeleteView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = models.SoftwareType.objects.all()


### DeviceSoftware
class DeviceSoftwareView(PermissionRequiredMixin, generic.ObjectView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = models.DeviceSoftware.objects.all()


class DeviceSoftwareListView(PermissionRequiredMixin, generic.ObjectListView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = models.DeviceSoftware.objects.all()
    table = tables.DeviceSoftwareTable
    filterset = filtersets.DeviceSoftwareFilterSet
    filterset_form = forms.DeviceSoftwareFilterForm


class DeviceSoftwareEditView(PermissionRequiredMixin, generic.ObjectEditView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = models.DeviceSoftware.objects.all()
    form = forms.DeviceSoftwareForm

    template_name = 'netbox_software/devicesoftware_edit.html'


class DeviceSoftwareDeleteView(PermissionRequiredMixin, generic.ObjectDeleteView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = models.DeviceSoftware.objects.all()
