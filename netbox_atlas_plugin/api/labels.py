class LabelDict(dict):

    def add_netbox_labels(self, obj):
        self.__setitem__('server_id', str(obj.id))
        if getattr(obj, "status", None) is not None:
            self.__setitem__('status', obj.status)

        if getattr(obj, "display_name", None) is not None:
            self.__setitem__('name', obj.display_name)

        if getattr(obj, "name", None) is not None:
            self.__setitem__('name', obj.name)

        if getattr(obj, "device_type", None) is not None:
            self.__setitem__('manufacturer', obj.device_type.manufacturer.slug)
            self.__setitem__('device_type', obj.device_type.slug)
            if getattr(obj.device_type, "model", None) is not None:
                self.__setitem__('model', obj.device_type.model)

        if getattr(obj, "role", None) is not None:
            self.__setitem__('role', obj.role.slug)

        if getattr(obj, "site", None) is not None:
            self.__setitem__('site', obj.site.slug)

        if getattr(obj, "platform", None) is not None:
            self.__setitem__('platform', obj.platform.slug)
        
        if getattr(obj, "serial", None) is not None:
            self.__setitem__('serial', obj.serial)

        if getattr(obj, "cluster", None) is not None:
            self.__setitem__("cluster",  obj.cluster.name)
            if obj.cluster.group:
                self.__setitem__("cluster_group",  obj.cluster.group.slug)
            if obj.cluster.type:
                self.__setitem__("cluster_type", obj.cluster.type.slug)

    def add_metrics_label(self, value):
        if value != '':
            self.__setitem__('metrics_label', value)

    def add_custom_labels(self, values):
        for key, value in values.items():
            self.__setitem__(key, value)
