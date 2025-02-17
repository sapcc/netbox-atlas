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
    
    @cached_property
    def get_configcontext_fields(self):
        cl = self.context['request'].query_params.get('configcontext_labels', None)
        fields = []
        if cl:
            fields = cl.split(';')
        return fields

    def get_url(self, dv):
        return {
            'url': self.context['request'].build_absolute_uri(dv.get_absolute_url())
        }

    def get_configcontext(self, dv):
        ctx = {}
        for pair in self.get_configcontext_fields:
            label = pair.split('=')
            if len(label) == 2:
                data = dv.local_context_data
                if data is None:
                    return ctx
                *path, last = label[1].split(".")
                for bit in path:
                    if bit.isdigit():
                        data = data[int(bit)]
                    else:
                        data = data.setdefault(bit, {})
                if last.isdigit():
                    last= int(last)
                try:
                    ctx[label[0]] = data[last]
                except KeyError as e:
                    pass

        return ctx

    def get_targets(self, dv):
        return get_targets(dv, self.get_target_field)

    def get_labels(self, dv):
        labels = LabelDict()

        if self.context['request'].query_params.get('target_in_name', False):
            labels.add_netbox_labels(dv, None)
        else:
            labels.add_netbox_labels(dv, self.get_target_field)
        labels.add_custom_labels(self.get_custom_fields)
        labels.add_custom_labels(self.get_configcontext(dv))
        labels.add_custom_labels(self.get_url(dv))
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


def get_targets(obj, interface_name):
    if interface_name == "primary_ip":
        if getattr(obj, "primary_ip", None) is not None:
            return [str(IPNetwork(obj.primary_ip.address).ip)]
        if getattr(obj, "primary_ip4", None) is not None:
            return [str(IPNetwork(obj.primary_ip4.address).ip)]
    elif interface_name == "mgmt_only":
        targets = []
        if hasattr(obj, "interfaces") and obj.interfaces is not None:
            result = obj.interfaces.filter(mgmt_only=True)
            targets = get_interface_addresses(result)
        return targets
    elif interface_name ==  "loopback10":
        targets = []
        if hasattr(obj, "interfaces") and obj.interfaces is not None:
            result = obj.interfaces.filter(name='Loopback10')
            targets = get_interface_addresses(result)
        return  targets
    elif interface_name == "cimc":
        targets = []
        if hasattr(obj, "interfaces") and obj.interfaces is not None:
            result = obj.interfaces.filter(name='cimc')
            targets = get_interface_addresses(result)
        return targets
    else:
        if hasattr(obj, "primary_ip") and obj.primary_ip is not None:
            return [str(IPNetwork(obj.primary_ip.address).ip)]

def get_interface_addresses(interfaces):
    interfaces = [i for i in map(map_ip_address, interfaces) if i is not None]
    return interfaces
    
def map_ip_address(interface):
    if len(interface.ip_addresses.all()) > 0:
        return str(IPNetwork(interface.ip_addresses.first().address).ip)
