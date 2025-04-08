class LabelDict(dict):

    def add_netbox_labels(self, obj, target_name=None, value_type="slug"):
        self.__setitem__('server_id', str(obj.id))
        if getattr(obj, "status", None) is not None:
            self.__setitem__('status', obj.status)

        if getattr(obj, "display_name", None) is not None:
            self.__setitem__('name', obj.display_name)
            if target_name:
                self.__setitem__('name', f"{obj.display_name}-{target_name}")

        if getattr(obj, "name", None) is not None:
            self.__setitem__('name', obj.name)
            if target_name:
                self.__setitem__('name', f"{obj.name}-{target_name}")

        if getattr(obj, "device_type", None) is not None:
            self.__setitem__('manufacturer', getattr(obj.device_type.manufacturer, value_type, ""))
            self.__setitem__('device_type', getattr(obj.device_type, value_type, ""))
            if getattr(obj.device_type, "model", None) is not None:
                self.__setitem__('model', obj.device_type.model)

        if getattr(obj, "role", None) is not None:
            self.__setitem__('role', getattr(obj.role, value_type, ""))

        if getattr(obj, "site", None) is not None:
            self.__setitem__('site', getattr(obj.site, value_type, ""))

        if getattr(obj, "platform", None) is not None:
            self.__setitem__('platform', getattr(obj.platform, value_type, ""))
        
        if getattr(obj, "serial", None) is not None:
            self.__setitem__('serial', obj.serial)

        if getattr(obj, "cluster", None) is not None:
            self.__setitem__("cluster",  obj.cluster.name)
            if obj.cluster.group:
                self.__setitem__("cluster_group", getattr(obj.cluster.group, value_type, ""))
            if obj.cluster.type:
                self.__setitem__("cluster_type", getattr(obj.cluster.type, value_type, ""))

    def add_metrics_label(self, value):
        if value != '':
            self.__setitem__('metrics_label', value)

    def add_custom_labels(self, values):
        for key, value in values.items():
            self.__setitem__(key, value)
