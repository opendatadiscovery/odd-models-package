"""
Client example for creating token, registering data source and ingesting data entities into the OpenDataDiscovery platform.
"""

from examples.postgres_models import data_entity_list, generator
from odd_models.api_client.v2.odd_api_client import Client

client = Client(host="http://localhost:8080")
client.auth(name="dev_aws_token", description="Token for dev AWS account data sources")

client.create_data_source(
    data_source_oddrn=generator.get_data_source_oddrn(),
    data_source_name="AWS dev account data source",
)
client.ingest_data_entity_list(data_entity_list)
