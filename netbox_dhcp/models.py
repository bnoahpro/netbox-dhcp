from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from netbox.models import NetBoxModel
from ipam.models import IPAddress, Prefix



class UpperCharField(models.CharField):
    def get_prep_value(self, value):
        return value.upper()


class DHCPServer(NetBoxModel):

    class Meta(NetBoxModel.Meta):
        verbose_name = "DHCP server"
        verbose_name_plural = "DHCP servers"

    name = models.CharField(
        unique=True,
    )
    api_token = models.CharField(
        verbose_name="API token",
    )
    api_url = models.URLField(
        verbose_name="API URL",
    )
    ssl_verify = models.BooleanField(
        verbose_name='SSL verify',
        default=True
    )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_dhcp:dhcpserver', args=[self.pk])


class DHCPReservation(NetBoxModel):
    class Meta(NetBoxModel.Meta):
        verbose_name = "DHCP reservation"

    ip_address = models.OneToOneField(
        to=IPAddress,
        verbose_name='IP Address',
        on_delete=models.CASCADE,
    )
    mac_address = UpperCharField(
        max_length=17,
        unique=True,
        verbose_name='MAC Address',
        validators=[
            RegexValidator(
                regex=r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$',
                message=_('Enter a valid MAC Addres like a1:b2:c3:d4:e5:f6.')
            )
        ],
    )
    status = models.CharField(
        max_length=17,
        default='pending',
    )
    dhcp_server = models.ForeignKey(
        to=DHCPServer,
        verbose_name='DHCP server',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('ip_address', 'mac_address')

    def get_absolute_url(self):
        return self.ip_address.get_absolute_url()

    def __str__(self):
        return f'{self.ip_address} {self.mac_address}'
