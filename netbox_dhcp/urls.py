from django.urls import path

from netbox_dhcp.views import DHCPReservationRecreateView, DHCPReservationCreateViewIPAddress, DHCPReservationEditView, DHCPReservationDeleteView, SynchronizeDHCP, DHCPServerListView, DHCPServerView, DHCPServerEditView, DHCPServerDeleteView, DHCPReservationCreateViewDHCPServer
from netbox_dhcp.models import DHCPServer, DHCPReservation
from netbox.views.generic import ObjectChangeLogView

urlpatterns = [
    ##### DHCPReservation #####
    path(route='<int:ip_address_id>/recreate',
         view=DHCPReservationRecreateView.as_view(),
         name='dhcpreservation_recreate'),
    path(route='<int:ip_address_id>/create',
         view=DHCPReservationCreateViewIPAddress.as_view(),
         name='dhcpreservation_create_ipaddress'),
    path(route='dhcp_server/<int:dhcp_server_id>/create',
         view=DHCPReservationCreateViewDHCPServer.as_view(),
         name='dhcpreservation_create'),
    path(route='dhcp_reservation/<int:pk>/edit',
         view=DHCPReservationEditView.as_view(),
         name='dhcpreservation_edit'),
    path(route='dhcp_reservation/<int:pk>/delete',
         view=DHCPReservationDeleteView.as_view(),
         name='dhcpreservation_delete'),
    path(route='dhcp_reservation/<int:pk>/changelog/',
         view=ObjectChangeLogView.as_view(),
         name='dhcpreservation_changelog',
         kwargs={'model': DHCPReservation}),

    ##### DHCPServer #####
    path(route='dhcp_server/<int:pk>',
         view=DHCPServerView.as_view(),
         name='dhcpserver'),
    path(route='dhcp_server/',
         view=DHCPServerListView.as_view(),
         name='dhcpserver_list'),
    path(route='dhcp_server/<int:pk>/edit',
         view=DHCPServerEditView.as_view(),
         name='dhcpserver_edit'),
    path(route='dhcp_server/add',
         view=DHCPServerEditView.as_view(),
         name='dhcpserver_add'),
    path(route='dhcp_server/<int:pk>/delete',
         view=DHCPServerDeleteView.as_view(),
         name='dhcpserver_delete'),
    path(route='dhcp_server/<int:pk>/changelog/',
         view=ObjectChangeLogView.as_view(),
         name='dhcpserver_changelog',
         kwargs={'model': DHCPServer}),

    ##### Synchronization #####
    path(route='dhcp_server/<int:pk>/synchonize',
         view=SynchronizeDHCP.as_view(),
         name='dhcpserver_synchronize'),
]


