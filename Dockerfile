FROM openapitools/openapi-generator:cli-v5.0.1 AS openapi_generator

# copying specification
COPY ./opendatadiscovery-specification/specification /spec

# generating stub for adapters
COPY ./openapi_generator/adapter/controller.mustache ./openapi_generator/adapter/__init__.mustache /templates/adapter/
RUN java -jar openapi-generator-cli.jar generate \
    -i /spec/odd_adapter.yaml \
    -g python-flask \
    -o /generated \
    -t /templates/adapter \
    --additional-properties=packageName=odd_models.adapter

# generating api client
COPY ./openapi_generator/api_client/api.mustache ./openapi_generator/api_client/__init__api.mustache /templates/api_client/
RUN java -jar openapi-generator-cli.jar generate \
    -i /spec/odd_api.yaml \
    -g python \
    -o /generated \
    -t /templates/api_client \
    --additional-properties=packageName=odd_models.api_client

# generating pydantic models
FROM python:3.9.1 as pydantic_generator
COPY ./opendatadiscovery-specification/specification /spec
RUN pip install datamodel-code-generator && mkdir generated
RUN datamodel-codegen --input /spec/entities.yaml --output generated/models.py --input-file-type openapi


FROM python:3.9.1

ARG ODD_MODELS_VERSION
ENV ODD_MODELS_VERSION=$ODD_MODELS_VERSION

ARG TWINE_USERNAME
ENV TWINE_USERNAME=$TWINE_USERNAME

ARG TWINE_PASSWORD
ENV TWINE_PASSWORD=$TWINE_PASSWORD

# collecting a package
WORKDIR package

# copying necessary files for adapter to package folder
COPY --from=openapi_generator  /generated/odd_models/adapter odd_models/adapter
COPY adapter/__init__.py odd_models/adapter

# removing models folder (because we are using pydantic models)
RUN rm -r odd_models/adapter/models

# copying necessary files for api client to package folder
COPY --from=openapi_generator  /generated/odd_models/api_client/api odd_models/api_client
COPY api_client/http_client.py odd_models/api_client
COPY api_client/__init__.py odd_models/

# copying generated pydantic models
COPY --from=pydantic_generator /generated/models.py odd_models/models.py

# copying package information
COPY ./openapi_generator/setup.py ./openapi_generator/README.md ./

# publishing the package to pypi
RUN pip install --user --upgrade twine && \
    python setup.py sdist bdist_wheel && \
    python -m twine upload dist/*

