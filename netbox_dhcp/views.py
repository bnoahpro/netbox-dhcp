from ipaddress import ip_address

from requests import get
from netbox.views.generic import ObjectEditView, ObjectDeleteView, ObjectView, ObjectListView
from ipam.models import IPAddress, Prefix
from netbox_dhcp.forms import DHCPReservationEditForm, DHCPReservationEditFormIPAddress, DHCPServerEditForm, DHCPReservationEditFormDHCPServer
from netbox_dhcp.models import DHCPReservation, DHCPServer
from netbox_dhcp.background_tasks import create_or_update_reservation, delete_reservation, delete_reservation_in_dhcp
from netbox_dhcp.tables import DHCPServerTable, DHCPReservationTable
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from logging import getLogger

logger = getLogger('netbox_dhcp')


# ---------------------------- #
#       DHCPReservation
# ---------------------------- #

class DHCPReservationView(ObjectView):
    queryset = DHCPReservation.objects.all()


class DHCPReservationCreateViewIPAddress(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'ipam.change_ipaddress'
    queryset = DHCPReservation.objects.all()
    form = DHCPReservationEditFormIPAddress

    def get_object(self, *args, **kwargs):
        ip_address = get_object_or_404(IPAddress, pk=kwargs['ip_address_id'])
        return DHCPReservation(ip_address=ip_address)


class DHCPReservationCreateViewDHCPServer(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'ipam.change_ipaddress'
    queryset = DHCPReservation.objects.all()
    form = DHCPReservationEditFormDHCPServer

    def get_object(self, *args, **kwargs):
        dhcp_server = get_object_or_404(DHCPServer, pk=kwargs['dhcp_server_id'])
        return DHCPReservation(dhcp_server=dhcp_server)

class DHCPReservationEditView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'ipam.change_ipaddress'
    queryset = DHCPReservation.objects.all()
    form = DHCPReservationEditForm


class DHCPReservationDeleteView(PermissionRequiredMixin, ObjectDeleteView):
    permission_required = 'ipam.change_ipaddress'
    queryset = DHCPReservation.objects.all()

    def get_return_url(self, request, obj=None):
        if obj and obj.ip_address:
            return obj.ip_address.get_absolute_url()
        return super().get_return_url(request, obj)


class DHCPReservationRecreateView(PermissionRequiredMixin, View):
    permission_required = 'ipam.change_ipaddress'


# ---------------------------- #
#         DHCPServer
# ---------------------------- #

class DHCPServerView(ObjectView):
    queryset = DHCPServer.objects.all()

    def get_extra_context(self, request, instance):
        table = DHCPReservationTable(instance.dhcpreservation_set.all())
        table.configure(request)

        return {
            'dhcp_reservation_table': table,
        }

    def get_absolute_url(self):
        return redirect(dhcp_server.get_absolute_url())


class DHCPServerListView(ObjectListView):
    queryset = DHCPServer.objects.all()
    table = DHCPServerTable


class DHCPServerEditView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'ipam.change_ipaddress'
    queryset = DHCPServer.objects.all()
    form = DHCPServerEditForm


class DHCPServerDeleteView(PermissionRequiredMixin, ObjectDeleteView):
    permission_required = 'ipam.change_ipaddress'
    queryset = DHCPServer.objects.all()


# ---------------------------- #
#       Synchronization
# ---------------------------- #

class SynchronizeDHCP(PermissionRequiredMixin, View):
    permission_required = 'ipam.change_ipaddress'

    def post(self, request, pk):
        dhcp_server = DHCPServer.objects.get(pk=pk)
        all_dhcp_reservations = dhcp_server.dhcpreservation_set.all()
        all_ip_addresses_id = list(all_dhcp_reservations.values_list('ip_address', flat=True))
        for dhcp_reservation in all_dhcp_reservations:
            create_or_update_reservation.delay(
                dhcp_reservation=dhcp_reservation
            )

        response_all_reservations_from_dhcp = get(f'{dhcp_server.api_url}/api/reservation/',
                                                  headers={'Authorization': f"Token {dhcp_server.api_token}"},
                                                  verify=dhcp_server.ssl_verify)
        if response_all_reservations_from_dhcp.ok:
            data_all_reservations_from_dhcp = response_all_reservations_from_dhcp.json()
            reservations_ids_from_dhcp = [reservation['netbox_id'] for reservation in data_all_reservations_from_dhcp]
            reservations_ids_to_delete = [id for id in reservations_ids_from_dhcp if id not in all_ip_addresses_id]
            delete_reservation_in_dhcp.delay(
                ids_to_delete=reservations_ids_to_delete,
                dhcp_server=dhcp_server
            )

        return redirect(dhcp_server.get_absolute_url())
