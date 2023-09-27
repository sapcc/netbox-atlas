from extras.plugins import PluginConfig


class NetBoxAtlasConfig(PluginConfig):
    name = "netbox_atlas_plugin"
    verbose_name = "Netbox Prometheus SD"
    description = (
        "A Netbox plugin to provide a Prometheus service discovery api"
    )
    version = ""
    author = "Stefan Hipfel"
    author_email = "stefan.hipfel@sap.com"
    base_url = "atlas"
    required_settings = []
    default_settings = {}


config = NetBoxAtlasConfig
