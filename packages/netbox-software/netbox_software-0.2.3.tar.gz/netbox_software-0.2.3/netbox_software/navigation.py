from extras.plugins import PluginMenuItem, PluginMenu, PluginMenuButton
from utilities.choices import ButtonColorChoices
from django.conf import settings

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_software', {})


class MyPluginMenu(PluginMenu):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name

    @property
    def name(self):
        return self._name


if plugin_settings.get('enable_navigation_menu'):

    menuitem = []
    # Add a menu item for Device software if enabled
    if plugin_settings.get('enable_device_software'):
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_software:devicesoftware_list',
                link_text='ПО устройств',
                buttons=[PluginMenuButton(
                    link='plugins:netbox_software:devicesoftware_add',
                    title='Создать',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )],
                permissions=['dcim.view_device']
            )
        )
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_software:softwaretype_list',
                link_text='Типы ПО',
                buttons=[PluginMenuButton(
                    link='plugins:netbox_software:softwaretype_add',
                    title='Создать',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )],
                permissions=['dcim.view_device']
            )
        )
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_software:vendor_list',
                link_text='Вендоры',
                buttons=[PluginMenuButton(
                    link='plugins:netbox_software:vendor_add',
                    title='Создать',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )],
                permissions=['dcim.view_device']
            )
        )
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_software:application_list',
                link_text='ПО',
                buttons=[PluginMenuButton(
                    link='plugins:netbox_software:application_add',
                    title='Создать',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )],
                permissions=['dcim.view_device']
            )
        )

    # If we are using NB 3.4.0+ display the new top level navigation option
    if settings.VERSION >= '3.4.0':
        menu = MyPluginMenu(
            name='SoftPl',
            label='Установленное ПО',
            groups=(
                ('', menuitem),
            ),
            icon_class='mdi mdi-microsoft-xbox-controller-off'
        )

    else:
        # Fall back to pre 3.4 navigation option
        menu_items = menuitem
