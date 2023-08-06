from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_software'

router = NetBoxRouter()
router.register('vendor', views.VendorViewSet)
router.register('softwaretype', views.SoftwareTypeViewSet)
router.register('application', views.ApplicationViewSet)
router.register('applicationversion', views.ApplicationVersionViewSet)
router.register('device-softwares', views.DeviceSoftwareViewSet)

urlpatterns = router.urls
