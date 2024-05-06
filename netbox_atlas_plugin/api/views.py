from virtualization.models import VirtualMachine
from dcim.models.devices import Device
from netbox.api.viewsets import NetBoxModelViewSet
from dcim.filtersets import DeviceFilterSet
from virtualization.filtersets import VirtualMachineFilterSet


from .serializers import (
    PrometheusDeviceSerializer,
    PrometheusVirtualMachineSerializer,
)


class VirtualMachineViewSet(
    NetBoxModelViewSet
):
    queryset = VirtualMachine.objects.prefetch_related(
        "cluster",
        "role",
        "platform",
        "primary_ip4",
    )

    filterset_class = VirtualMachineFilterSet
    serializer_class = PrometheusVirtualMachineSerializer
    pagination_class = None


class DeviceViewSet(NetBoxModelViewSet):
    queryset = Device.objects.prefetch_related(
        "device_type",
        "role",
        "primary_ip4",
        "platform",
        "site",
        "cluster",
    )
    filterset_class = DeviceFilterSet
    serializer_class = PrometheusDeviceSerializer
    pagination_class = None
