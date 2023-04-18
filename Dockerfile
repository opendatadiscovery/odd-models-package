# generating pydantic models
FROM openapitools/openapi-generator:cli-v5.0.1 AS openapi_generator

COPY ./opendatadiscovery-specification/specification /spec
COPY ./openapi_generator/api_client/api.mustache ./openapi_generator/api_client/__init__api.mustache /templates/api_client/
RUN java -jar openapi-generator-cli.jar generate \
    -i /spec/odd_api.yaml \
    -g python \
    -o /generated \
    -t /templates/api_client \
    --additional-properties=packageName=odd_models.api_client

FROM python:3.9.16 as pydantic_generator
ENV GENERATTOR_VERSION=0.14.1
ENV TARGET_PYTHON_VERSION=3.9
COPY ./opendatadiscovery-specification/specification /spec
RUN pip install datamodel-code-generator==$GENERATTOR_VERSION
RUN mkdir generated

RUN datamodel-codegen \
    --input /spec/entities.yaml \
    --output generated/models.py \
    --input-file-type openapi \
    --target-python-version $TARGET_PYTHON_VERSION

RUN datamodel-codegen \
    --input /spec/metrics.yaml \
    --output generated/metrics.py \
    --input-file-type openapi \
    --target-python-version $TARGET_PYTHON_VERSION


FROM python:3.9.16 as builder

ARG ODD_MODELS_VERSION
ENV ODD_MODELS_VERSION=$ODD_MODELS_VERSION

ARG PYPI_USERNAME
ENV PYPI_USERNAME=$PYPI_USERNAME

ARG PYPI_PASSWORD
ENV PYPI_PASSWORD=$PYPI_PASSWORD

ENV POETRY_HOME=/etc/poetry \
    POETRY_VERSION=1.3.1
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# collecting a package
WORKDIR odd-models
RUN apt-get update && \
    apt-get install -y -q build-essential curl
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 -
RUN poetry config experimental.new-installer false

COPY pyproject.toml poetry.lock ./

COPY LICENSE README.md ./
COPY ./odd_models ./odd_models

# copying generated assets
COPY --from=pydantic_generator /generated/ odd_models/models/
COPY --from=openapi_generator  /generated/odd_models/api_client/api odd_models/api_client

# publishing package
RUN poetry build

# for real PyPI index
RUN poetry publish --username $PYPI_USERNAME --password $PYPI_PASSWORD
