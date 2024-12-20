from netbox.api.routers import NetBoxRouter
from netbox_dhcp.api.views import DHCPServerViewSet, DHCPReservationViewSet

app_name = 'netbox_dhcp'

router = NetBoxRouter()
router.register('server', DHCPServerViewSet)
router.register('reservation', DHCPReservationViewSet)

urlpatterns = router.urls
