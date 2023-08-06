import django_tables2 as tables

from netbox.tables import NetBoxTable, columns
from tenancy.tables import TenantColumn
from .models import DeviceSoftware, Vendor, SoftwareType

SOFTWARE_TYPE_SOFTWARE_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_software:softwaretype' pk=record.pk %}">{% firstof record.name record.name %}</a>
{% endif %}
"""

VENDOR_SOFTWARE_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_software:vendor' pk=record.pk %}">{% firstof record.name record.name %}</a>
{% endif %}
"""

DEVICE_SOFTWARE_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_software:devicesoftware' pk=record.pk %}">{% firstof record.name record.name %}</a>
{% endif %}
"""

SOFTWARE_ASSIGN_LINK = """
<a href="{% url ''plugins:netbox_software:devicesoftware' pk=record.pk %}?{% if request.GET.device_soft %}device={{ request.GET.device_soft }}{% elif request.GET.vm_soft %}vm_soft={{ request.GET.vm_soft }}{% endif %}&return_url={{ request.GET.return_url }}">{{ record }}</a>
"""

class VendorTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=VENDOR_SOFTWARE_LINK)

    class Meta(NetBoxTable.Meta):
        model = Vendor
        fields = ('pk', 'id', 'name', 'comments', 'actions', 'created', 'last_updated',)
        default_columns = ('name',)


class SoftwareTypeTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=SOFTWARE_TYPE_SOFTWARE_LINK)

    class Meta(NetBoxTable.Meta):
        model = SoftwareType
        fields = ('pk', 'id', 'name', 'comments', 'actions', 'created', 'last_updated',)
        default_columns = ('name',)


class DeviceSoftwareTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=DEVICE_SOFTWARE_LINK)
    software_type = tables.Column(
        linkify=True
    )
    vendor = tables.Column(
        linkify=True
    )
    device = tables.Column(
        linkify=True
    )
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name='Устройство'
    )

    tags = columns.TagColumn(
        url_name='dcim:sitegroup_list'
    )

    class Meta(NetBoxTable.Meta):
        model = DeviceSoftware
        fields = ('pk', 'id', 'name', 'software_type', 'vendor', 'version', 'comments', 'actions',
                  'created', 'last_updated', 'tags')
        default_columns = ('name', 'software_type', 'assigned_object', 'vendor', 'tags')


class DeviceSoftwareAssignTable(NetBoxTable):
    name = tables.TemplateColumn(
        template_code=SOFTWARE_ASSIGN_LINK,
        verbose_name='ПО'
    )
    status = columns.ChoiceFieldColumn()
    assigned_object = tables.Column(
        orderable=False
    )

    class Meta(NetBoxTable.Meta):
        model = DeviceSoftware
        fields = ('name', 'software_type', 'vendor', 'version', 'assigned_object', 'description')
        exclude = ('id', )
        orderable = False


class AssignedDeviceSoftwareTable(NetBoxTable):
    """
    List DeviceSoftware assigned to an object.
    """
    name = tables.Column(
        linkify=True,
        verbose_name='ПО'
    )

    class Meta(NetBoxTable.Meta):
        model = DeviceSoftware
        fields = ('name', 'software_type', 'vendor', 'version', 'assigned_object', 'description')
        exclude = ('id', )

