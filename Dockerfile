FROM openjdk:11.0.4-jre-slim AS openapi_generator

COPY ./opendatadiscovery-specification/specification /spec
COPY ./openapi-generator/openapi-generator-cli.jar /provectus-openapi-generator/openapi-generator-cli.jar
COPY ./openapi-generator/serializers.mustache ./openapi-generator/controller.mustache /templates/
RUN java -jar /provectus-openapi-generator/openapi-generator-cli.jar generate \
    -i /spec/odd_adapter.yaml \
    -g python-flask \
    -o /generated \
    -t /templates \
    --global-property=apiTests=false \
    --additional-properties=packageName=odd_contract

RUN ls /generated
RUN ls /generated/odd_contract

FROM python:3.9.1

ARG ODD_CONTRACT_VERSION
ENV ODD_CONTRACT_VERSION=$ODD_CONTRACT_VERSION

ARG TWINE_USERNAME
ENV TWINE_USERNAME=$TWINE_USERNAME

ARG TWINE_PASSWORD
ENV TWINE_PASSWORD=$TWINE_PASSWORD

WORKDIR package
COPY --from=openapi_generator  /generated/odd_contract odd_contract
COPY odd_contract/__init__.py odd_contract
COPY setup.py README.md ./

RUN pip install --user --upgrade twine && \
    python3 setup.py sdist bdist_wheel && \
    python3 -m twine upload --repository testpypi dist/*