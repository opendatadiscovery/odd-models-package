from unittest.mock import Mock

import pytest

from odd_models.discovery.data_assets.aws_lambda import AWSLambda


@pytest.fixture
def client():
    from odd_models.api_client.v2.odd_api_client import Client

    client = Mock(Client)
    return client


def test_data_source(client):
    from odd_models.discovery.data_source import DataSource

    with DataSource(oddrn="//oddrn", client=client) as ctx:
        ctx.add_data_asset(
            AWSLambda.from_params(
                region="us-east-1", account="123456789012", function_name="my_function"
            )
        )

    client.ingest_data_entity_list.assert_called_once()
