from odd_models.discovery.data_assets import AWSLambda, S3Artifact
from odd_models.models import DataEntityType


def test_lambda():
    some_lambda = AWSLambda.from_params(
        region="us-east-1", account="123456789012", function_name="my_function"
    )

    some_lambda.add_upstream(S3Artifact.from_url("s3://bucket/folder/input.csv"))
    some_lambda.add_downstream(S3Artifact.from_url("s3://bucket/folder/output.csv"))

    data_entity = some_lambda.to_data_entity()
    assert data_entity.type == DataEntityType.JOB
    assert len(data_entity.data_transformer.inputs) == 1
    assert len(data_entity.data_transformer.outputs) == 1

    S3Artifact.from_url("s3://bucket/folder/input_two.csv") >> some_lambda
    data_entity = some_lambda.to_data_entity()
    assert len(data_entity.data_transformer.inputs) == 2
    assert len(data_entity.data_transformer.outputs) == 1

    some_lambda >> S3Artifact.from_url("s3://bucket/folder/output_two.csv")
    data_entity = some_lambda.to_data_entity()
    assert len(data_entity.data_transformer.inputs) == 2
    assert len(data_entity.data_transformer.outputs) == 2
