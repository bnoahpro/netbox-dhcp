from rest_framework import serializers

from ipam.models import IPAddress
from netbox.api.serializers import NetBoxModelSerializer
from netbox_dhcp.models import DHCPReservation, DHCPServer


class DHCPReservationSerializer(NetBoxModelSerializer):

    ip_address = serializers.PrimaryKeyRelatedField(queryset=IPAddress.objects.all())
    dhcp_server = serializers.PrimaryKeyRelatedField(queryset=DHCPServer.objects.all())

    class Meta:
        model = DHCPReservation
        fields = (
            'id',
            'mac_address',
            'ip_address',
            'dhcp_server',
            'created',
            'last_updated'
        )
        read_only_fields = (
            'id',
            'created',
            'last_updated'
        )


class DHCPServerSerializer(NetBoxModelSerializer):
    class Meta:
        model = DHCPServer
        fields = (
            'id',
            'name',
            'display',
            'api_token',
            'api_url',
            'tags',
            'created',
            'last_updated',
        )

    read_only_fields = (
        'id',
        'created',
        'last_updated'
    )