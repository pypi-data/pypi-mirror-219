import django_tables2 as tables

from netbox.tables import NetBoxTable, columns
from tenancy.tables import TenantColumn
from .models import DeviceSoftware, Vendor, SoftwareType, ApplicationVersion, Application

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

APPLICATION_VERSION_SOFTWARE_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_software:applicationversion' pk=record.pk %}">{% firstof record.name record.name %}</a>
{% endif %}
"""

APPLICATION_SOFTWARE_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_software:application' pk=record.pk %}">{% firstof record.name record.name %}</a>
{% endif %}
"""

DEVICE_SOFTWARE_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_software:devicesoftware' pk=record.pk %}">{% firstof record.app record.app %}</a>
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


class ApplicationVersionTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=APPLICATION_VERSION_SOFTWARE_LINK)

    class Meta(NetBoxTable.Meta):
        model = ApplicationVersion
        fields = ('pk', 'id', 'name', 'comments', 'actions', 'created', 'last_updated',)
        default_columns = ('name',)


class ApplicationTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=APPLICATION_SOFTWARE_LINK)
    software_type = tables.Column(
        linkify=True
    )
    vendor = tables.Column(
        linkify=True
    )
    tags = columns.TagColumn(
        url_name='dcim:sitegroup_list'
    )

    class Meta(NetBoxTable.Meta):
        model = Application
        fields = ('pk', 'id', 'name', 'software_type', 'vendor', 'comments', 'actions', 'created', 'last_updated',
                  'tags')
        default_columns = ('name', 'software_type', 'vendor')


class DeviceSoftwareTable(NetBoxTable):
    # name = tables.TemplateColumn(template_code=DEVICE_SOFTWARE_LINK)
    app = tables.Column(
        linkify=True
    )
    version = tables.Column(
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
        fields = ('pk', 'id', 'app', 'version', 'comments', 'actions', 'created', 'last_updated', 'tags')
        default_columns = ('app', 'software_type', 'assigned_object', 'version', 'tags')


class DeviceSoftwareAssignTable(NetBoxTable):
    app = tables.Column(
        orderable=False
    )
    version = tables.Column(
        orderable=False
    )
    status = columns.ChoiceFieldColumn()
    assigned_object = tables.Column(
        orderable=False
    )

    class Meta(NetBoxTable.Meta):
        model = DeviceSoftware
        fields = ('app', 'version', 'assigned_object', 'description')
        exclude = ('id', )
        orderable = False


class AssignedDeviceSoftwareTable(NetBoxTable):
    """
    List DeviceSoftware assigned to an object.
    """
    app = tables.Column(
        linkify=True,
        verbose_name='ПО'
    )

    class Meta(NetBoxTable.Meta):
        model = DeviceSoftware
        fields = ('app', 'software_type', 'vendor', 'version', 'assigned_object', 'description')
        exclude = ('id', )

