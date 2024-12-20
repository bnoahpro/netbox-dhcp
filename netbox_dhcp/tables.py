from django_tables2 import LinkColumn

from netbox.tables import NetBoxTable
from netbox_dhcp.models import DHCPServer, DHCPReservation


class DHCPServerTable(NetBoxTable):
    name = LinkColumn()

    class Meta(NetBoxTable.Meta):
        model = DHCPServer
        fields = ('name', 'api_token', 'api_url')


class DHCPReservationTable(NetBoxTable):
    ip_address = LinkColumn()

    class Meta(NetBoxTable.Meta):
        model = DHCPReservation
        fields = ('ip_address', 'mac_address', 'status')
