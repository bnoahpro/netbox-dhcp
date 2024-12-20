import time
from logging import getLogger
from ipam.models import IPAddress
from netbox_dhcp.models import DHCPReservation, DHCPServer
from django_rq import job
from requests import post, put, delete, get, Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from time import sleep

logger = getLogger('netbox_dhcp')


@job
def create_or_update_reservation(dhcp_reservation: DHCPReservation):
    try:
        ip_address = dhcp_reservation.ip_address
        dhcp_server = dhcp_reservation.dhcp_server
        reservation_conf = {'mac': dhcp_reservation.mac_address, 'ip': str(ip_address),
                            'hostname_fqdn': ip_address.dns_name}
        if dhcp_reservation.status == "active":
            response = put(f'{dhcp_server.api_url}/api/reservation/{ip_address.id}/',
                           headers={'Authorization': f"Token {dhcp_server.api_token}"},
                           json=reservation_conf,
                           verify=dhcp_server.ssl_verify)
        else:
            reservation_conf['netbox_id'] = ip_address.id
            response = post(f'{dhcp_server.api_url}/api/reservation/',
                            headers={'Authorization': f"Token {dhcp_server.api_token}"},
                            json=reservation_conf,
                            verify=dhcp_server.ssl_verify)
        if not response.ok:
            logger.debug(f"response.json: {response.text}")
        logger.debug(f"data_results: {response.json()}")
        data = dict()
        while not data.get("is_celery_task_succeed", False):
            feedback = get(f'{dhcp_server.api_url}/api/reservation/{ip_address.id}/',
                           headers={'Authorization': f"Token {dhcp_server.api_token}"},
                           verify=dhcp_server.ssl_verify)
            data = feedback.json()
            time.sleep(1)
        if data['is_celery_task_succeed']:
            DHCPReservation.objects.filter(pk=dhcp_reservation.id).update(status='active')
    except Exception as e:
        DHCPReservation.objects.filter(pk=dhcp_reservation.id).update(status='error')
        raise


@job
def delete_reservation(dhcp_reservation: DHCPReservation):
    try:
        ip_address = dhcp_reservation.ip_address
        dhcp_server = dhcp_reservation.dhcp_server
        response = delete(f'{dhcp_server.api_url}/api/reservation/{ip_address.id}/',
                          headers={'Authorization': f"Token {dhcp_server.api_token}"},
                          verify=dhcp_server.ssl_verify)
        if not response.ok:
            logger.debug(f"response.json: {response}")
        status_code = response.status_code
        logger.debug(f"data_results: {status_code}")
    except Exception as e:
        DHCPReservation.objects.filter(pk=dhcp_reservation.id).update(status='error')
        raise


@job
def delete_reservation_in_dhcp(ids_to_delete: list(), dhcp_server: DHCPServer):
    """
    Function that delete all reservations in DHCP server if their netbox_id is not in Netbox

    ids_to_delete: list of reservations to delete in DHCP server
    dhcp_server: DHCPServer object to target
    """
    try:
        for id in ids_to_delete:
            response = delete(f'{dhcp_server.api_url}/api/reservation/{id}/',
                              headers={'Authorization': f"Token {dhcp_server.api_token}"},
                              verify=dhcp_server.ssl_verify)
    except Exception as e:
        DHCPReservation.objects.filter(pk=dhcp_reservation.id).update(status='error')
        raise
