[![PyPI version](https://badge.fury.io/py/odd-models.svg)](https://badge.fury.io/py/odd-models)

# OpenDataDiscovery Models package
Has some useful tools for working with OpenDataDiscovery. Such as:
1. Generated Python models from OpenDataDiscovery specification.
2. API Client for working with OpenDataDiscovery.
3. API for manual discovering data entities.

### Installation
```bash
pip install odd-models
```

### Models using example
**odd-models.models** package provides automatically generated Python model by OpenDataDiscovery specification.
It can be used for creating data entities for uploading them into the Platform.

Code example ([full code](./examples/postgres_models.py)):
```python
from oddrn_generator import PostgresqlGenerator
from odd_models.models import DataEntity, DataSet, DataSetField, DataSetFieldType, DataEntityType, Type, MetadataExtension
generator = PostgresqlGenerator(host_settings="localhost", databases="my_database", schemas="public")
DataEntity(
    oddrn=generator.get_oddrn_by_path("tables", "my_table"),
    name="my_table",
    type=DataEntityType.TABLE,
    metadata=[MetadataExtension(schema_url="https://example.com/schema.json", metadata={"env": "DEV"})],
    dataset=DataSet(
        field_list=[
            DataSetField(
                oddrn=generator.get_oddrn_by_path("tables_columns", "name"),
                name="name",
                type=DataSetFieldType(
                    type=Type.TYPE_STRING,
                    logical_type='str',
                    is_nullable=False
                ),
            )
        ]
    )
)
```


### HTTP Client for OpenDataDiscovery
___
**odd-models.client** package provides API client for OpenDataDiscovery API.
Client provides an API for working with OpenDataDiscovery Platform.
It has various methods for working with data sources, data entities, management etc.

Code example([full code](./examples/client.py)):

```python
from examples.postgres_models import data_entity_list, generator
from odd_models.api_client.v2.odd_api_client import Client

client = Client(host="http://localhost:8080")
client.auth(name="postgres", description="Token for dev AWS account data sources")

client.create_data_source(
    data_source_oddrn=generator.get_data_source_oddrn(),
    data_source_name="Postgres data source",
)
client.ingest_data_entity_list(data_entities=data_entity_list)
```

### Manual Discovery API
___
When there is no programmatic way to discover data sources and data entities, **odd-models.discovery** package provides API for manual discovery of data sources and data entities.

Code example([full code](./examples/lambda_discovery.py)):

```python
from odd_models.discovery import DataSource
from odd_models.discovery.data_assets import AWSLambda, S3Artifact
from odd_models.discovery.data_assets.data_asset_list import DataAssetsList

with DataSource("//cloud/aws/dev") as data_source:
    validation_lambda = AWSLambda.from_params(
        region="eu-central-1", account="0123456789", function_name="validation"
    )
    input_artifact = S3Artifact.from_url("s3://bucket/folder/test_data.csv")

    results = S3Artifact.from_url("s3://bucket/folder/test_result.csv")
    metrics = S3Artifact.from_url("s3://bucket/folder/test_metrics.json")

    input_artifact >> validation_lambda >> DataAssetsList([results, metrics])

    data_source.add_data_asset(validation_lambda)
```

# Development

### Installation
```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Generating models
```bash
# Generate models. Will generate models pydantic into odd_models/models
make generate_models

# Generate api client. Will generate api client into odd_models/api_client
make generate_client
```

### Tests
```bash
pytest .
```

### Docker build
```bash
docker build -t odd-models .
```
