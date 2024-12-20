from netbox.plugins.templates import PluginTemplateExtension


class ReservationInfo(PluginTemplateExtension):
    model = 'ipam.ipaddress'

    def buttons(self):
        return self.render('netbox_dhcp/dhcpreservation_recreate_button.html')

    def right_page(self):
        return (
            self.render('netbox_dhcp/dhcp_reservation.html')
        )


template_extensions = [ReservationInfo]
