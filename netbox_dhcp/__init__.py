from netbox.plugins import PluginConfig

class NetBoxDHCP(PluginConfig):
    name = 'netbox_dhcp'
    verbose_name = 'NetBox DHCP'
    description = 'Manage Dnsmasq DHCP with NetBox'
    version = '0.1'
    base_url = 'netbox-dhcp'

    def ready(self):
        super().ready()
        from . import signals

config = NetBoxDHCP