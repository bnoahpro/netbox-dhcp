from netbox.forms import NetBoxModelForm
from netbox_dhcp.models import DHCPReservation, DHCPServer


class DHCPReservationEditFormDHCPServer(NetBoxModelForm):
    class Meta:
        model = DHCPReservation
        fields = ['mac_address', 'ip_address']


class DHCPReservationEditForm(NetBoxModelForm):
    class Meta:
        model = DHCPReservation
        fields = ['mac_address']

class DHCPReservationEditFormIPAddress(NetBoxModelForm):
    class Meta:
        model = DHCPReservation
        fields = ['mac_address', 'dhcp_server']


class DHCPServerEditForm(NetBoxModelForm):
    class Meta:
        model = DHCPServer
        fields = ['name', 'api_token', 'api_url', 'ssl_verify']
