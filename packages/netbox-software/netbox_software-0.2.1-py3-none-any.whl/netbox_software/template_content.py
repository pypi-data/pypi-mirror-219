from extras.plugins import PluginTemplateExtension
from django.conf import settings
from .models import DeviceSoftware

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_software', {})


class DeviceSoftwareList(PluginTemplateExtension):
    model = 'dcim.device'
    def left_page(self):
        if plugin_settings.get('enable_device_software') and plugin_settings.get('device_software_location') == 'left':

            return self.render('netbox_software/devicesoftware_include.html', extra_context={
                'device_software': DeviceSoftware.objects.filter(assigned_object_id=self.context['object'].id,
                                                                 assigned_object_type__model='device')[:20],
                'soft_count': DeviceSoftware.objects.filter(assigned_object_id=self.context['object'].id,
                                                            assigned_object_type__model='device').count(),
            })
        else:
            return ""

    def right_page(self):
        if plugin_settings.get('enable_device_software') and plugin_settings.get('device_software_location') == 'right':

            return self.render('netbox_software/devicesoftware_include.html', extra_context={
                'device_software': DeviceSoftware.objects.filter(assigned_object=self.context['object'].id,
                                                                 assigned_object_type__model='device')[:20],
                'soft_count': DeviceSoftware.objects.filter(assigned_object=self.context['object'].id,
                                                            assigned_object_type__model='device').count(),
            })
        else:
            return ""


class VirtualMachineSoftwareList(PluginTemplateExtension):
    model = 'virtualization.virtualmachine'

    def left_page(self):
        if plugin_settings.get('enable_device_software') and plugin_settings.get('device_software_location') == 'left':

            return self.render('netbox_software/devicesoftware_include.html', extra_context={
                'device_software': DeviceSoftware.objects.filter(assigned_object_id=self.context['object'].id,
                                                                 assigned_object_type__model='virtualmachine')[:20],
                'soft_count': DeviceSoftware.objects.filter(assigned_object_id=self.context['object'].id,
                                                            assigned_object_type__model='virtualmachine').count(),
            })
        else:
            return ""

    def right_page(self):
        if plugin_settings.get('enable_device_software') and plugin_settings.get('device_software_location') == 'right':

            return self.render('netbox_software/devicesoftware_include.html', extra_context={
                'device_software': DeviceSoftware.objects.filter(assigned_object=self.context['object'].id,
                                                                 assigned_object_type__model='virtualmachine')[:20],
                'soft_count': DeviceSoftware.objects.filter(assigned_object=self.context['object'].id,
                                                            assigned_object_type__model='virtualmachine').count(),
            })
        else:
            return ""
#     def left_page(self):
#         if plugin_settings.get('enable_device_software') and plugin_settings.get('device_software_location') == 'left':
#
#             return self.render('netbox_software/devicesoftware_include.html', extra_context={
#                 'device_software': DeviceSoftware.objects.filter(assigned_object=self.context['object'])[:20],
#                 'soft_count': DeviceSoftware.objects.filter(assigned_object=self.context['object']).count(),
#             })
#         else:
#             return ""
#
#     def right_page(self):
#         if plugin_settings.get('enable_device_software') and plugin_settings.get('device_software_location') == 'right':
#
#             return self.render('netbox_software/devicesoftware_include.html', extra_context={
#                 'device_software': DeviceSoftware.objects.filter(assigned_object=self.context['object'])[:20],
#                 'soft_count': DeviceSoftware.objects.filter(assigned_object=self.context['object']).count(),
#             })
#         else:
#             return ""
#     def left_page(self):
#         if plugin_settings.get('enable_virtual-machine_software') and plugin_settings.get('virtual-machine_software_location') == 'left':
#
#             return self.render('netbox_software/virtualmachinesoftware_include.html', extra_context={
#                 'virtual_machine_software': VirtualMachineSoftware.objects.filter(
#                     virtual_machine=self.context['object']
#                 )[:20],
#                 'soft_count': VirtualMachineSoftware.objects.filter(virtual_machine=self.context['object']).count(),
#             })
#         else:
#             return ""
#
#     def right_page(self):
#         if plugin_settings.get('enable_virtual-machine_software') and plugin_settings.get('virtual-machine_software_location') == 'right':
#
#             return self.render('netbox_software/virtualmachinesoftware_include.html', extra_context={
#                 'virtual_machine_software': VirtualMachineSoftware.objects.filter(
#                     virtual_machine=self.context['object']
#                 )[:20],
#                 'soft_count': VirtualMachineSoftware.objects.filter(virtual_machine=self.context['object']).count(),
#             })
#         else:
#             return ""


template_extensions = [DeviceSoftwareList]
