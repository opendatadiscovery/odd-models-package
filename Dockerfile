# generating pydantic models
FROM python:3.9.1 as pydantic_generator
COPY ./opendatadiscovery-specification/specification /spec
RUN pip install datamodel-code-generator && mkdir generated
RUN datamodel-codegen --input /spec/entities.yaml --output generated/models.py --input-file-type openapi


FROM python:3.9.1

ARG ODD_MODELS_VERSION
ENV ODD_MODELS_VERSION=$ODD_MODELS_VERSION

ARG PYPI_USERNAME
ENV PYPI_USERNAME=$PYPI_USERNAME

ARG PYPI_PASSWORD
ENV PYPI_PASSWORD=$PYPI_PASSWORD

# collecting a package
WORKDIR package

# copying generated pydantic models
COPY --from=pydantic_generator /generated/models.py odd_models/models.py

# copying another package files
COPY ./pyproject.toml ./odd_models_src/README.md ./
COPY ./odd_models_src/__init__.py ./odd_models_src/utils.py odd_models/

# installing poetry
ENV POETRY_PATH=/opt/poetry POETRY_VERSION=1.1.6
ENV PATH="$POETRY_PATH/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update && \
    apt-get install -y -q build-essential curl
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
RUN mv /root/.poetry $POETRY_PATH

# publishing package
RUN poetry build

# for test PyPI index (local development)
# RUN poetry config repositories.testpypi https://test.pypi.org/legacy/
# RUN poetry publish --repository testpypi --username $PYPI_USERNAME --password $PYPI_PASSWORD

# for real PyPI index
RUN poetry publish --username $PYPI_USERNAME --password $PYPI_PASSWORD
