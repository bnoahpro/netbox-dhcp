from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from netbox_dhcp.models import DHCPReservation
from netbox_dhcp.background_tasks import create_or_update_reservation, delete_reservation


@receiver(post_save, sender=DHCPReservation)
def trigger_create_or_update_reservation(instance: DHCPReservation, **_kwargs):
    create_or_update_reservation.delay(
        dhcp_reservation=instance
    )


@receiver(post_delete, sender=DHCPReservation)
def trigger_delete_reservation(instance: DHCPReservation, **_kwargs):
    delete_reservation.delay(
        dhcp_reservation=instance
    )
