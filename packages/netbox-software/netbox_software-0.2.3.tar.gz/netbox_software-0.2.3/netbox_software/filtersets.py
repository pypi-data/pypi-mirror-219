import django_filters
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from netbox.filtersets import NetBoxModelFilterSet
from utilities.filters import MultiValueNumberFilter, MultiValueCharFilter
from dcim.models import Device
from virtualization.models import VirtualMachine
from .models import DeviceSoftware, SoftwareType, Vendor, ApplicationVersion, Application
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


class ApplicationVersionFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = ApplicationVersion
        fields = ('id', 'name',)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(comments__icontains=value)
        )


class ApplicationFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Application
        fields = ('id', 'name', 'software_type', 'vendor')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(comments__icontains=value)
        )


class DeviceSoftwareFilterSet(NetBoxModelFilterSet):
    app = MultiValueCharFilter(
        method='filter_app',
        field_name='name',
        label=_('App (name)'),
    )
    app_id = MultiValueNumberFilter(
        method='filter_app',
        field_name='pk',
        label=_('App (ID)'),
    )
    version = MultiValueCharFilter(
        method='filter_version',
        field_name='name',
        label=_('Version (name)'),
    )
    version_id = MultiValueNumberFilter(
        method='filter_version',
        field_name='pk',
        label=_('Version (ID)'),
    )

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
        fields = ('id',)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(app__name__icontains=value) |
            Q(version__name__icontains=value)
        )

    def filter_app(self, queryset, name, value):
        apps = Application.objects.filter(**{'{}__in'.format(name): value})
        if not apps.exists():
            return queryset.none()
        return queryset.filter(
            app__in=apps
        )

    def filter_version(self, queryset, name, value):
        versions = ApplicationVersion.objects.filter(**{'{}__in'.format(name): value})
        if not versions.exists():
            return queryset.none()
        return queryset.filter(
            version__in=versions
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

