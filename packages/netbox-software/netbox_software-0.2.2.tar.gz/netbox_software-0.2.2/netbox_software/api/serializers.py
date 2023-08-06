from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from django.contrib.contenttypes.models import ContentType

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from netbox.api.fields import ChoiceField, ContentTypeField, SerializedPKRelatedField
from netbox.constants import NESTED_SERIALIZER_PREFIX
from utilities.api import get_serializer_for_model
from ..models import DeviceSoftware, SoftwareType, Vendor, SOFTWARE_ASSIGNMENT_MODELS, ApplicationVersion, Application


# Vendor Serializer
class VendorSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_software-api:vendor-detail')

    class Meta:
        model = Vendor
        fields = ('id', 'url', 'display', 'name', 'comments', 'custom_fields', 'created', 'last_updated',)


class NestedVendorSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_software-api:vendor-detail')

    class Meta:
        model = Vendor
        fields = ('id', 'url', 'display', 'name',)


# SoftwareType Serializer
class SoftwareTypeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_software-api:softwaretype-detail'
    )

    class Meta:
        model = SoftwareType
        fields = ('id', 'url', 'display', 'name', 'comments', 'custom_fields', 'created', 'last_updated',)


class NestedSoftwareTypeSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_software-api:softwaretype-detail'
    )

    class Meta:
        model = SoftwareType
        fields = ('id', 'url', 'display', 'name',)


# Application Serializer
class ApplicationVersionSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_software-api:applicationversion-detail'
    )

    class Meta:
        model = ApplicationVersion
        fields = ('id', 'url', 'display', 'name', 'comments', 'custom_fields', 'created', 'last_updated',)


class NestedApplicationVersionSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_software-api:applicationversion-detail'
    )

    class Meta:
        model = ApplicationVersion
        fields = ('id', 'url', 'display', 'name',)


# Device Software Serializer
class ApplicationSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_software-api:application-detail'
    )
    software_type = NestedSoftwareTypeSerializer()
    vendor = NestedVendorSerializer()

    class Meta:
        model = Application
        fields = (
            'id', 'url', 'display', 'name', 'software_type', 'vendor', 'comments', 'tags', 'custom_fields',
            'created', 'last_updated',
        )


class NestedApplicationSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_software-api:application-detail'
    )

    class Meta:
        model = Application
        fields = ('id', 'url', 'display', 'name',)


# Device Software Serializer
class DeviceSoftwareSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_software-api:devicesoftware-detail'
    )
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(SOFTWARE_ASSIGNMENT_MODELS),
        required=False,
        allow_null=True
    )
    assigned_object = serializers.SerializerMethodField(read_only=True)

    app = NestedApplicationSerializer()
    version = NestedApplicationVersionSerializer()

    class Meta:
        model = DeviceSoftware
        fields = (
            'id', 'url', 'display', 'app', 'version', 'assigned_object_type', 'assigned_object_id', 'assigned_object',
            'comments', 'tags', 'custom_fields', 'created', 'last_updated',
        )

    @extend_schema_field(serializers.JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object, prefix=NESTED_SERIALIZER_PREFIX)
        context = {'request': self.context['request']}
        return serializer(obj.assigned_object, context=context).data


class NestedDeviceSoftwareSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_software-api:devicesoftware-detail'
    )

    class Meta:
        model = DeviceSoftware
        fields = ('id', 'url', 'display',)

