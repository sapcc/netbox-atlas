# Netbox Atlas

A Plugin that provides API endpoint for Prometheus service discovery. e.g.:

- `http://netbox_url/api/plugins/atlas/devices/?region=eu-de-2&custom_labels=test=some_value&status=active&platform=vmware-esxi&role=server&metrics_label=some_extra_label`
- `http://netbox_url/api/plugins/atlas/virtual-machines/?region=eu-de-2&custom_labels=test=some_value&status=active`

## Develop

1. `docker-compose up postgres -d`
2. Import netbox data to postgres:
   `cat netbox_dump.sql | docker exec -i {container_id} psql -U netbox`
3. `docker-compose up -d`
