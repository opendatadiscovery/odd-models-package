FROM openapitools/openapi-generator:cli-v5.0.1 AS openapi_generator

COPY ./opendatadiscovery-specification/specification /spec
COPY ./openapi_generator/controller.mustache ./openapi_generator/__init__.mustache /templates/
RUN java -jar openapi-generator-cli.jar generate \
    -i /spec/odd_adapter.yaml \
    -g python-flask \
    -o /generated \
    -t /templates \
    --additional-properties=packageName=odd_models

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

WORKDIR package
COPY --from=openapi_generator  /generated/odd_models odd_models
RUN rm -r odd_models/models
COPY --from=pydantic_generator /generated/models.py odd_models/models.py
COPY odd_models/__init__.py odd_models
COPY setup.py README.md ./

RUN pip install --user --upgrade twine && \
    python setup.py sdist bdist_wheel && \
    python -m twine upload dist/*
