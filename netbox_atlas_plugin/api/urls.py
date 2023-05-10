from rest_framework import routers
from .views import VirtualMachineViewSet, DeviceViewSet

router = routers.DefaultRouter()
router.register("virtual-machines", VirtualMachineViewSet)
router.register("devices", DeviceViewSet)

urlpatterns = router.urls
