import django_filters
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from netbox.filtersets import NetBoxModelFilterSet
from utilities.filters import MultiValueNumberFilter, MultiValueCharFilter
from dcim.models import Device
from virtualization.models import VirtualMachine
from .models import DeviceSoftware, SoftwareType, Vendor
from django.db.models import Q


class VendorFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Vendor
        fields = ('id', 'name',)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(comments__icontains=value)
        )


class SoftwareTypeFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SoftwareType
        fields = ('id', 'name',)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(comments__icontains=value)
        )


class DeviceSoftwareFilterSet(NetBoxModelFilterSet):
    device = MultiValueCharFilter(
        method='filter_device',
        field_name='name',
        label=_('Device (name)'),
    )
    device_id = MultiValueNumberFilter(
        method='filter_device',
        field_name='pk',
        label=_('Device (ID)'),
    )
    virtual_machine = MultiValueCharFilter(
        method='filter_virtual_machine',
        field_name='name',
        label=_('Virtual machine (name)'),
    )
    virtual_machine_id = MultiValueNumberFilter(
        method='filter_virtual_machine',
        field_name='pk',
        label=_('Virtual machine (ID)'),
    )

    class Meta:
        model = DeviceSoftware
        fields = ('id', 'name', 'software_type', 'vendor')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(version__icontains=value)
        )

    def filter_device(self, queryset, name, value):
        devices = Device.objects.filter(**{'{}__in'.format(name): value})
        if not devices.exists():
            return queryset.none()
        devices_ids = []
        for device in devices:
            devices_ids.append(device.id)
        return queryset.filter(
            assigned_object_id__in=devices_ids,
            assigned_object_type__model='device'
        )

    def filter_virtual_machine(self, queryset, name, value):
        virtual_machines = VirtualMachine.objects.filter(**{'{}__in'.format(name): value})
        if not virtual_machines.exists():
            return queryset.none()
        vm_ids = []
        for vm in virtual_machines:
            vm_ids.append(vm.id)
        return queryset.filter(
            assigned_object_id__in=vm_ids,
            assigned_object_type__model='virtualmachine'
        )

