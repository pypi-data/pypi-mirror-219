from django.urls import path
from . import models, views
from netbox.views.generic import ObjectChangeLogView

urlpatterns = (

    # Vendor
    path('vendor/', views.VendorListView.as_view(), name='vendor_list'),
    path('vendor/add/', views.VendorEditView.as_view(), name='vendor_add'),
    path('vendor/<int:pk>/', views.VendorView.as_view(), name='vendor'),
    path('vendor/<int:pk>/edit/', views.VendorEditView.as_view(), name='vendor_edit'),
    path('vendor/<int:pk>/delete/', views.VendorDeleteView.as_view(), name='vendor_delete'),
    path('vendor/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='vendor_changelog', kwargs={
        'model': models.Vendor
    }),

    # SoftwareType
    path('softwaretype/', views.SoftwareTypeListView.as_view(), name='softwaretype_list'),
    path('softwaretype/add/', views.SoftwareTypeEditView.as_view(), name='softwaretype_add'),
    path('softwaretype/<int:pk>/', views.SoftwareTypeView.as_view(), name='softwaretype'),
    path('softwaretype/<int:pk>/edit/', views.SoftwareTypeEditView.as_view(), name='softwaretype_edit'),
    path('softwaretype/<int:pk>/delete/', views.SoftwareTypeDeleteView.as_view(), name='softwaretype_delete'),
    path('softwaretype/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='softwaretype_changelog', kwargs={
        'model': models.SoftwareType
    }),

    # ApplicationVersion
    path('applicationversion/', views.ApplicationVersionListView.as_view(), name='applicationversion_list'),
    path('applicationversion/add/', views.ApplicationVersionEditView.as_view(), name='applicationversion_add'),
    path('applicationversion/<int:pk>/', views.ApplicationVersionView.as_view(), name='applicationversion'),
    path('applicationversion/<int:pk>/edit/', views.ApplicationVersionEditView.as_view(),
         name='applicationversion_edit'),
    path('applicationversion/<int:pk>/delete/', views.ApplicationVersionDeleteView.as_view(),
         name='applicationversion_delete'),
    path('applicationversion/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='applicationversion_changelog',
         kwargs={'model': models.ApplicationVersion}),

    # App
    path('application/', views.ApplicationListView.as_view(), name='application_list'),
    path('application/add/', views.ApplicationEditView.as_view(), name='application_add'),
    path('application/<int:pk>/', views.ApplicationView.as_view(), name='application'),
    path('application/<int:pk>/edit/', views.ApplicationEditView.as_view(), name='application_edit'),
    path('application/<int:pk>/delete/', views.ApplicationDeleteView.as_view(), name='application_delete'),
    path('application/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='application_changelog', kwargs={
        'model': models.Application
    }),

    # DeviceSoftware
    path('device-software/', views.DeviceSoftwareListView.as_view(), name='devicesoftware_list'),
    path('device-software/add/', views.DeviceSoftwareEditView.as_view(), name='devicesoftware_add'),
    path('device-software/<int:pk>/', views.DeviceSoftwareView.as_view(), name='devicesoftware'),
    path('device-software/<int:pk>/edit/', views.DeviceSoftwareEditView.as_view(), name='devicesoftware_edit'),
    path('device-software/<int:pk>/delete/', views.DeviceSoftwareDeleteView.as_view(), name='devicesoftware_delete'),
    path('device-software/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='devicesoftware_changelog', kwargs={
        'model': models.DeviceSoftware
    }),

)
