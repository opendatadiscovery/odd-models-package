class EmptyTokenError(ValueError):
    def __init__(self):
        super().__init__(
            "Couldn't create HttpClient. Host was not set. Possible solutions:\n"
            "1. Set env variable :export ODD_PLATFORM_HOST=http://localhost:8080",
        )


class EmptyHostError(ValueError):
    def __init__(self):
        super().__init__(
            "Couldn't create HttpClient. Token was not set. Possible solutions:\n"
            "1. Create token either using client API or platform UI\n"
            "2. Set env variable: export ODD_PLATFORM_TOKEN=<TOKEN_FROM_STEPS_ABOVE>",
        )


class CreateDataSourceError(Exception):
    def __init__(
        self, data_source_name: str, data_source_oddrn: str, message: str
    ) -> None:
        super().__init__(
            f"Couldn't register datasource {data_source_name} with oddrn {data_source_oddrn} \n"
            f"Message: {message}"
        )


class IngestionEntitiesError(Exception):
    def __init__(self, data_source_oddrn: str, message: str) -> None:
        super().__init__(
            f"Couldn't ingest entities for {data_source_oddrn=}.\n"
            f"Message: {message}"
        )


class CreateTokenError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"Couldn't create token.\n" f"Message: {message}")


class GetDegChildrenError(Exception):
    def __init__(self, oddrn: str, message: str) -> None:
        super().__init__(
            f"Couldn't retrieve children for def with{oddrn=}.\n" f"Message: {message}"
        )
