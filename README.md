[![PyPI version](https://badge.fury.io/py/odd-models.svg)](https://badge.fury.io/py/odd-models)

# ODD models package

Generates python models by [ODD OpenApi specification](https://github.com/opendatadiscovery/opendatadiscovery-specification)

## Usage
### Install
```bash
pip install odd-models
#or using poetry
poetry add odd-models
```


### Import and usage example:
```python
from odd_models.models import DataEntityList

data_entity_list = DataEntityList(data_source_oddrn='/postgresql/host/localhost/databases/opendatadiscovery', items=[])
```


## Build
```bash
docker build . -t odd-models-dev:build --build-arg PYPI_USERNAME=<PYPI_USERNAME> --build-arg PYPI_PASSWORD=<PYPI_PASSWORD>
```
