class LabelDict(dict):
    DEFAULT_LABELS = {
        'server_id': 'id',
        'status': 'status',
        'name': 'name{{-FOO}}',

        'manufacturer': 'device_type:manufacturer:slug',
        'device_type': 'device_type:slug',
        'model': 'device_type:model{{-BAR}}',

        'role': 'role:slug',
        'site': 'site:slug',
        'platform': 'platform:slug',
        'serial': 'serial',
        'cluster': 'cluster:name',
        'cluster_group': 'cluster:group:slug',
        'cluster_type': 'cluster:type:slug',
    }

    def __init__(self, *args, **kwargs):
        super().__init__()
        # Allow overwriting defaults with provided values
        self.update(*args, **kwargs)

    def add_netbox_labels(self, obj, overrides=None):
        # Start with default labels
        self.update(self.DEFAULT_LABELS)
        # Apply overrides if provided
        if overrides and isinstance(overrides, dict):
            self.update(overrides)

        # Dynamically populate labels from the object
        for label, obj_key in self.items():
            if ":" in obj_key:
                # Handle nested attributes
                keys = obj_key.split(':')
                value = obj
                for key in keys:
                    if "{{" in key:
                        # Handle hardcoded string addition
                        key, hardcoded = key.split("{{")
                        hardcoded = hardcoded.strip("}}")
                        if hasattr(value, key):
                            value = getattr(value, key)
                            value = f"{value}{hardcoded}"  # Append the hardcoded string
                        else:
                            value = None
                            break
                    elif hasattr(value, key):
                        value = getattr(value, key)
                    else:
                        value = None
                        break
                if value is not None:
                    self.__setitem__(label, value)
                else:
                    self.__setitem__(label, "")
            else:
                # Handle direct attributes
                value = None
                if "{{" in obj_key:
                    # Handle hardcoded string addition
                    key, hardcoded = obj_key.split("{{")
                    hardcoded = hardcoded.strip("}}")
                    if hasattr(obj, key):
                        value = getattr(obj, key)
                        value = f"{value}{hardcoded}"  # Append the hardcoded string
                    else:
                        value = None
                if hasattr(obj, obj_key):
                    value = getattr(obj, obj_key)
                self.__setitem__(label, value)

    def add_metrics_label(self, value):
        if value != '':
            self.__setitem__('metrics_label', value)

    def add_custom_labels(self, values):
        for key, value in values.items():
            self.__setitem__(key, value)
