from netbox.api.viewsets import NetBoxModelViewSet

from .. import models, filtersets
from .serializers import DeviceSoftwareSerializer, SoftwareTypeSerializer, VendorSerializer, \
    ApplicationVersionSerializer, ApplicationSerializer


class VendorViewSet(NetBoxModelViewSet):
    queryset = models.Vendor.objects.all()
    serializer_class = VendorSerializer
    filterset_class = filtersets.VendorFilterSet


class SoftwareTypeViewSet(NetBoxModelViewSet):
    queryset = models.SoftwareType.objects.all()
    serializer_class = SoftwareTypeSerializer
    filterset_class = filtersets.SoftwareTypeFilterSet


class ApplicationVersionViewSet(NetBoxModelViewSet):
    queryset = models.ApplicationVersion.objects.prefetch_related('tags')
    serializer_class = ApplicationVersionSerializer
    filterset_class = filtersets.ApplicationVersionFilterSet


class ApplicationViewSet(NetBoxModelViewSet):
    queryset = models.Application.objects.prefetch_related('tags', 'software_type', 'vendor')
    serializer_class = ApplicationSerializer
    filterset_class = filtersets.ApplicationFilterSet


class DeviceSoftwareViewSet(NetBoxModelViewSet):
    queryset = models.DeviceSoftware.objects.prefetch_related('tags', 'app', 'version', 'assigned_object')
    serializer_class = DeviceSoftwareSerializer
    filterset_class = filtersets.DeviceSoftwareFilterSet
