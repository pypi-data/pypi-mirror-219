from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet


SOFTWARE_ASSIGNMENT_MODELS = Q(
    Q(app_label='dcim', model='device') |
    Q(app_label='virtualization', model='virtualmachine')
)


class Vendor(NetBoxModel):
    name = models.CharField(verbose_name="название", max_length=150, help_text='Укажите производителя ПО')
    comments = models.TextField(verbose_name="комментарий", blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Разработчики"
        verbose_name = "Разработчик"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_software:vendor', args=[self.pk])

    def get_devices_count(self):
        return DeviceSoftware.objects.filter(vendor=self).count()

    def get_devices(self):
        devices = []
        dev_softs = DeviceSoftware.objects.filter(vendor=self)
        for soft in dev_softs:
            devices.append(soft.device.name)
        return DeviceSoftware.objects.filter(vendor=self)

    def get_software_count(self):
        return DeviceSoftware.objects.filter(app__vendor=self).values('app__name', 'version__name').distinct().count()
        # result = []
        # # data = DeviceSoftware.objects.filter(app__vendor=self).values('app__name', 'version__name').distinct()
        #
        # keys = []
        # for item in data:
        #     # if item['app__name'] in keys:
        #     #     continue
        #     keys.append(item['app__name'])
        #     result.append([item['app__name'],item['version__name']])
        # return len(result)

    def get_software(self):
        # return DeviceSoftware.objects.filter(app__vendor=self).distinct()
        result = []
        data = DeviceSoftware.objects.filter(app__vendor=self).distinct()
        keys = {}
        for item in data:
            if item.app.name in keys.keys() and item.version.name in keys[item.app.name]['versions']:
                continue
            if item.app.name in keys.keys():
                keys[item.app.name]['versions'].append(item.version.name)
                result.append(item)
                continue
            keys[item.app.name] = {'versions': [item.version.name]}

            result.append(item)
        return result


class SoftwareType(NetBoxModel):
    name = models.CharField(verbose_name="название", max_length=100, help_text='Укажите тип ПО')
    comments = models.TextField(verbose_name="комментарий", blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Типы ПО"
        verbose_name = "Тип ПО"

    def __str__(self):
        return self.name

    def get_apps(self):
        return Application.objects.filter(software_type=self)

    def get_absolute_url(self):
        return reverse('plugins:netbox_software:softwaretype', args=[self.pk])

    def get_devices_count(self):
        return DeviceSoftware.objects.filter(software_type=self).count()

    def get_devices(self):
        return DeviceSoftware.objects.filter(software_type=self)


class Application(NetBoxModel):
    name = models.CharField(
        verbose_name="название",
        max_length=100,
        help_text='Укажите имя, которое будет отображаться для этого ПО.'
    )

    software_type = models.ForeignKey(
        to=SoftwareType,
        verbose_name="тип ПО",
        on_delete=models.CASCADE,
        related_name='app_soft_types'
    )

    vendor = models.ForeignKey(
        to=Vendor,
        verbose_name="Разработчик",
        on_delete=models.CASCADE,
        related_name='app_vendor'
    )

    comments = models.TextField(verbose_name="комментарий", blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Приложения"
        verbose_name = "Приложение"

    def __str__(self):
        return self.name

    def get_all_versions(self):
        return list(set(DeviceSoftware.objects.filter(app=self).values_list('version__name', flat=True)))


class ApplicationVersion(NetBoxModel):
    name = models.CharField(verbose_name="название", max_length=50, help_text='Укажите тип ПО')
    comments = models.TextField(verbose_name="комментарий", blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Версии ПО"
        verbose_name = "Версия ПО"

    def __str__(self):
        return self.name


class DeviceSoftware(NetBoxModel):
    app = models.ForeignKey(
        to=Application,
        verbose_name="Приложение",
        on_delete=models.CASCADE,
        related_name='devices'
    )

    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=SOFTWARE_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )

    assigned_object_id = models.PositiveBigIntegerField(
        blank=True,
        null=True
    )
    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type',
        fk_field='assigned_object_id'
    )

    version = models.ForeignKey(
        verbose_name="версия",
        to=ApplicationVersion,
        on_delete=models.CASCADE,
        related_name='devices_with_version'
    )

    comments = models.TextField(
        verbose_name="комментарий",
        blank=True
    )

    class Meta:
        ordering = ('app',)
        verbose_name_plural = "ПО устройств"
        verbose_name = "ПО устройства"

    def __str__(self):
        return f'{self.app.name} v{self.version.name}'

    def to_objectchange(self, action):
        objectchange = super().to_objectchange(action)
        objectchange.related_object = self.assigned_object
        return objectchange

    def get_absolute_url(self):
        return reverse('plugins:netbox_software:devicesoftware', args=[self.pk])

    def get_devices(self):
        return DeviceSoftware.objects.filter(vendor=self.vendor).count()

    def get_software(self):
        return list(DeviceSoftware.objects.filter(vendor=self.vendor))

    def get_software_count(self):
        return DeviceSoftware.objects.filter(app=self.app, version=self.version).count()
