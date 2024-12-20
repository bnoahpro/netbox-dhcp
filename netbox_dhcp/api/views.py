from netbox.api.viewsets import NetBoxModelViewSet
from netbox_dhcp.models import DHCPServer, DHCPReservation
from netbox_dhcp.api.serializers import DHCPServerSerializer, DHCPReservationSerializer


class DHCPReservationViewSet(NetBoxModelViewSet):
    queryset = DHCPReservation.objects.prefetch_related('tags')
    serializer_class = DHCPReservationSerializer


class DHCPServerViewSet(NetBoxModelViewSet):
    queryset = DHCPServer.objects.prefetch_related('tags')
    serializer_class = DHCPServerSerializer
