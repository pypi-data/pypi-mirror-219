from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_software'

router = NetBoxRouter()
router.register('vendor', views.VendorViewSet)
router.register('softwaretype', views.SoftwareTypeViewSet)
router.register('device-softwares', views.DeviceSoftwareViewSet)

urlpatterns = router.urls
