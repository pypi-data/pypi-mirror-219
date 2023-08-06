from netbox.search import SearchIndex
from .models import DeviceSoftware, Vendor, SoftwareType, Application, ApplicationVersion
from django.conf import settings

# If we run NB 3.4+ register search indexes 
if settings.VERSION >= '3.4.0':
    class VendorIndex(SearchIndex):
        model = Vendor
        fields = (
            ("name", 100),
            ("comments", 5000),
        )

    class SoftwareTypeIndex(SearchIndex):
        model = SoftwareType
        fields = (
            ("name", 100),
            ("comments", 5000),
        )

    class ApplicationIndex(SearchIndex):
        model = Application
        fields = (
            ("name", 100),
            ("comments", 5000),
        )

    class ApplicationVersionIndex(SearchIndex):
        model = ApplicationVersion
        fields = (
            ("name", 100),
            ("comments", 5000),
        )

    class DeviceSoftwareIndex(SearchIndex):
        model = DeviceSoftware
        fields = (
            ("app__name", 100),
            ("version__name", 500),
            ("comments", 5000),
        )

    # Register indexes
    indexes = [VendorIndex, SoftwareTypeIndex, ApplicationIndex, ApplicationVersionIndex, DeviceSoftwareIndex]
