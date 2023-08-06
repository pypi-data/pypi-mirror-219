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
        return DeviceSoftware.objects.filter(vendor=self).count()

    def get_software(self):
        soft_list = []
        dev_softs = DeviceSoftware.objects.filter(vendor=self)
        for soft in dev_softs:
            soft_list.append(soft)
        return soft_list


class SoftwareType(NetBoxModel):
    name = models.CharField(verbose_name="название", max_length=100, help_text='Укажите тип ПО')
    comments = models.TextField(verbose_name="комментарий", blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Типы ПО"
        verbose_name = "Тип ПО"

    def __str__(self):
        return self.name

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
        related_name='device_software'
    )

    vendor = models.ForeignKey(
        to=Vendor,
        verbose_name="Разработчик",
        on_delete=models.CASCADE,
        related_name='device_software'
    )

    comments = models.TextField(verbose_name="комментарий", blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "ПО"

    def __str__(self):
        return self.name


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
        related_name='device_app_version'
    )

    comments = models.TextField(
        verbose_name="комментарий",
        blank=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "ПО устройств"
        verbose_name = "ПО устройства"

    def __str__(self):
        return self.name

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
        return DeviceSoftware.objects.filter(app=self.app).count()
