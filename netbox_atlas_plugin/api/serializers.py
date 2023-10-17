from functools import cached_property
from rest_framework import serializers
from virtualization.models import VirtualMachine
from dcim.models import Device
from netaddr import IPNetwork

from .labels import LabelDict


class PrometheusDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ["targets", "labels"]

    targets = serializers.SerializerMethodField()
    labels = serializers.SerializerMethodField()

    @cached_property
    def get_target_field(self):
        return self.context['request'].query_params.get('target', 'primary_ip')

    @cached_property
    def get_metrics_field(self):
        return self.context['request'].query_params.get('metrics_label', '')

    @cached_property
    def get_custom_fields(self):
        cl = self.context['request'].query_params.get('custom_labels', None)
        fields = {}
        if cl:
            pairs = cl.split(';')
            for pair in pairs:
                label = pair.split('=')
                if len(label) == 2:
                    fields[label[0]] = label[1]
        return fields

    def get_targets(self, dv):
        return get_targets(dv, self.get_target_field)

    def get_labels(self, dv):
        labels = LabelDict()

        labels.add_netbox_labels(dv)
        labels.add_custom_labels(self.get_custom_fields)
        labels.add_metrics_label(self.get_metrics_field)

        return labels


class PrometheusVirtualMachineSerializer(serializers.ModelSerializer):

    class Meta:
        model = VirtualMachine
        fields = ["targets", "labels"]

    targets = serializers.SerializerMethodField()
    labels = serializers.SerializerMethodField()

    @cached_property
    def get_target_field(self):
        return self.context['request'].query_params.get('target', 'primary_ip')

    @cached_property
    def get_metrics_field(self):
        return self.context['request'].query_params.get('metrics_label', '')

    @cached_property
    def get_custom_fields(self):
        cl = self.context['request'].query_params.get('custom_labels', None)
        fields = {}
        if cl:
            pairs = cl.split(';')
            for pair in pairs:
                label = pair.split('=')
                if len(label) == 2:
                    fields[label[0]] = label[1]
        return fields

    def get_targets(self, vm):
        return get_targets(vm, self.get_target_field)

    def get_labels(self, obj):
        labels = LabelDict()

        labels.add_netbox_labels(obj)
        labels.add_custom_labels(self.get_custom_fields)
        labels.add_metrics_label(self.get_metrics_field)
        return labels


def get_targets(vm, target):
    if target == "primary_ip":
        if getattr(vm, "primary_ip", None) is not None:
            return [str(IPNetwork(vm.primary_ip.address).ip)]
        if getattr(vm, "primary_ip4", None) is not None:
            return [str(IPNetwork(vm.primary_ip4.address).ip)]
    elif target == "mgmt_only":
        targets = []
        if hasattr(vm, "interfaces") and vm.interfaces is not None:
            result = vm.interfaces.filter(mgmt_only=True)
            targets = get_interface_addresses(result)
        return targets
    elif target ==  "loopback10":
        targets = []
        if hasattr(vm, "interfaces") and vm.interfaces is not None:
            result = vm.interfaces.filter(name='Loopback10')
            targets = get_interface_addresses(result)
        return  targets
    else:
        if hasattr(vm, "primary_ip") and vm.primary_ip is not None:
            return [str(IPNetwork(vm.primary_ip.address).ip)]


def get_interface_addresses(interfaces):
    interfaces = [i for i in map(map_ip_address, interfaces) if i is not None]
    return interfaces
    
def map_ip_address(interface):
    if len(interface.ip_addresses.all()) > 0:
        return str(IPNetwork(interface.ip_addresses.first().address).ip)