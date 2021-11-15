# Open Data Discovery Models Package

## Models
You can use odd pydantic models:
```python
from odd_models.models import DataEntityList

data_entity_list = DataEntityList(data_source_oddrn='/postgresql/host/localhost/databases/opendatadiscovery', items=[])
```

## Adapter's Controller
You can inherit from base Adapter Controller for writing your own adapters:
```python
from odd_models.adapter.controllers import ODDController

class MyController(ODDController):
    def get_data_entities(self, changed_since=None, )
        pass
```

## ODD API Client
You can use ready API Client to send requests:
```python
from odd_models.api_client import ODDApiClient

api_client = ODDApiClient(base_url='http://127.0.0.1:8080')

# using pydantic objects:
from odd_models.models import DataEntityList
data_entity_list = DataEntityList(data_source_oddrn='/postgresql/host/localhost/databases/opendatadiscovery', items=[])

response = api_client.post_data_entity_list(data_entity_list)
assert response.status_code == 200

# using dict (validation will be in the client)
data_entity_list = {'data_source_oddrn': '/postgresql/host/localhost/databases/opendatadiscovery', 'items': []}

response = api_client.post_data_entity_list(data_entity_list)
assert response.status_code == 200
```