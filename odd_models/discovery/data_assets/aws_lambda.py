from oddrn_generator import LambdaGenerator

from odd_models.discovery.data_assets.data_asset import (
    HasUpstream,
    MappableToDataEntity,
    Transformer,
)
from odd_models.discovery.helper import link_nodes
from odd_models.models import DataEntity, DataEntityType, DataTransformer


class AWSLambda(Transformer, MappableToDataEntity):
    """DataAsset for AWS Lambda functions

    Args:
        oddrn (str): The ODDRN of the Lambda function, i.e //lambda/cloud/aws/account/123456789012/region/us-east-1/functions/my_function
        func_name (str): The name of the Lambda function, i.e my_function
    """

    def __init__(self, oddrn: str, func_name: str) -> None:
        self.upstream: list[str] = []
        self.downstream: list[str] = []

        self.oddrn = oddrn
        self.func_name = func_name

    def to_data_entity(self) -> DataEntity:
        return DataEntity(
            oddrn=self.oddrn,
            name=self.func_name,
            type=DataEntityType.JOB,
            data_transformer=DataTransformer(
                inputs=self.upstream, outputs=self.downstream
            ),
        )

    def __rshift__(self, other: HasUpstream) -> HasUpstream:
        return link_nodes(self, other)

    @classmethod
    def from_params(cls, region: str, account: str, function_name: str) -> "AWSLambda":
        oddrn = LambdaGenerator.from_params(
            region, account, function_name
        ).get_oddrn_by_path("functions")
        return cls(oddrn=oddrn, func_name=function_name)
