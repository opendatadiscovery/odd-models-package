from textwrap import dedent


class EmptyTokenError(ValueError):

    def __init__(self):
        message = dedent('''
            Couldn't send request. Token was not set. Possible solutions:
            1. Create token either using client API or platform UI
            2. Set env variable: export ODD_PLATFORM_TOKEN=<TOKEN_FROM_STEP_ABOVE>
            3. Provide token url explicitly to Client
            4. Use auth method on client object"
        ''')

        super().__init__(message)


class EmptyHostError(ValueError):
    def __init__(self):
        message = dedent('''
            Couldn't create HttpClient. Host was not set. Possible solutions:
            1. Set env variable :export ODD_PLATFORM_HOST=http://localhost:8080
            2. Provide host url explicitly to Client
        ''')
        super().__init__(message)


class CreateDataSourceError(Exception):
    def __init__(
            self, data_source_name: str, data_source_oddrn: str, message: str
    ) -> None:
        message = dedent(f'''
            Couldn't register {data_source_name=} with an {data_source_oddrn=}"
            Message: {message}
        ''')
        super().__init__(message)


class IngestionEntitiesError(Exception):
    def __init__(self, data_source_oddrn: str, message: str) -> None:
        message = dedent(f'''
            Couldn't ingest entities for {data_source_oddrn=}
            Message: {message}
        ''')
        super().__init__(
            message
        )


class CreateTokenError(Exception):
    def __init__(self, message: str) -> None:
        message = dedent(f'''
            Couldn't create token.
            Message: {message}
        ''')
        super().__init__(message)


class GetDegChildrenError(Exception):
    def __init__(self, oddrn: str, message: str) -> None:
        message = dedent(f'''
        Couldn't retrieve children for DEG with an {oddrn=}.
        Message: {message}
        ''')
        super().__init__(message)
