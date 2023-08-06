from extras.plugins import PluginConfig


class NetboxSoftware(PluginConfig):
    name = 'netbox_software'
    verbose_name = 'Установленное ПО'
    description = 'Manage device software in Netbox'
    version = '0.2.1'
    author = 'Ilya Zakharov'
    author_email = 'me@izakharov.ru'
    min_version = '3.2.0'
    base_url = 'software'
    default_settings = {
        "enable_navigation_menu": True,
        "enable_device_software": True,
        # "enable_virtual-machine_software": True,
        "device_software_location": "left",
        # "virtual-machine_software_location": "left",
    }


config = NetboxSoftware
