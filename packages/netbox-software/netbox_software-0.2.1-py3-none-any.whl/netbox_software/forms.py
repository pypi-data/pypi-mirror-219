from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from dcim.models import Device
from virtualization.models import VirtualMachine
from .models import DeviceSoftware, SoftwareType, Vendor

from django.conf import settings
from packaging import version

NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)
if NETBOX_CURRENT_VERSION >= version.parse("3.5"):
    from utilities.forms.fields import TagFilterField, CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
else:
    from utilities.forms import TagFilterField, CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField


# Vendor Form & Filter Form
class VendorForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = Vendor
        fields = ('name', 'comments',)


class VendorFilterForm(NetBoxModelFilterSetForm):
    model = Vendor
    name = forms.CharField(
        label='Название',
        required=False
    )


# SoftwareType Form & Filter Form
class SoftwareTypeForm(NetBoxModelForm):
    comments = CommentField()
    class Meta:
        model = SoftwareType
        fields = ('name', 'comments',)


class SoftwareTypeFilterForm(NetBoxModelFilterSetForm):
    model = SoftwareType
    name = forms.CharField(
        label='Название',
        required=False
    )


# Device Software Form & Filter Form
class DeviceSoftwareForm(NetBoxModelForm):
    comments = CommentField()

    device = DynamicModelChoiceField(
        label='Устройство',
        queryset=Device.objects.all(),
        required=False
    )

    virtual_machine = DynamicModelChoiceField(
        label='Устройство',
        queryset=VirtualMachine.objects.all(),
        required=False
    )

    software_type = DynamicModelChoiceField(
        label='Тип',
        queryset=SoftwareType.objects.all(),
        required=True
    )
    vendor = DynamicModelChoiceField(
        label='Разработчик',
        queryset=Vendor.objects.all(),
        required=True
    )

    class Meta:
        model = DeviceSoftware
        fields = ('name', 'vendor', 'software_type', 'version', 'comments', 'tags')

    def __init__(self, *args, **kwargs):
        # Initialize helper selectors
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {}).copy()
        if instance:
            if type(instance.assigned_object) is Device:
                initial['device'] = instance.assigned_object
            elif type(instance.assigned_object) is VirtualMachine:
                initial['virtual_machine'] = instance.assigned_object
        kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        # Handle object assignment
        selected_objects = [
            field for field in ('device', 'virtual_machine') if self.cleaned_data[field]
        ]
        if len(selected_objects) > 1:
            raise forms.ValidationError({
                selected_objects[1]: "A Soft can only be assigned to a single object."
            })
        elif selected_objects:
            self.instance.assigned_object = self.cleaned_data[selected_objects[0]]
        else:
            self.instance.assigned_object = None


class DeviceSoftwareFilterForm(NetBoxModelFilterSetForm):
    model = DeviceSoftware
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        ('Атрибуты', ('name', 'software_type_id', 'vendor_id')),
        ('Устройство/ВМ', ('device_id', 'virtual_machine_id')),
    )

    name = forms.CharField(
        label='Название',
        required=False
    )

    device_id = DynamicModelMultipleChoiceField(
        label='Устройство',
        queryset=Device.objects.all(),
        required=False
    )

    virtual_machine_id = DynamicModelMultipleChoiceField(
        label='ВМ',
        queryset=VirtualMachine.objects.all(),
        required=False
    )

    software_type_id = forms.ModelMultipleChoiceField(
        label='Тип',
        queryset=SoftwareType.objects.all(),
        required=False
    )
    vendor_id = forms.ModelMultipleChoiceField(
        label='Разработчик',
        queryset=Vendor.objects.all(),
        required=False
    )

    tag = TagFilterField(model)
