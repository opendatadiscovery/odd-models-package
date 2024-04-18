from odd_models.discovery.data_assets import AWSLambda, S3Artifact
from odd_models.discovery.data_assets.data_asset_list import DataAssetsList


def test_data_assets_list():
    inputs_dal = DataAssetsList(
        [
            S3Artifact.from_url("s3://bucket/inputs/key_one"),
            S3Artifact.from_url("s3://bucket/inputs/key_two"),
        ]
    )

    assert len(inputs_dal) == 2

    s3_lambda = AWSLambda("transformer", "//aws/lambda/transformer")
    inputs_dal >> s3_lambda

    outputs_dal = DataAssetsList(
        [
            S3Artifact.from_url("s3://bucket/outputs/key_one"),
            S3Artifact.from_url("s3://bucket/outputs/key_two"),
        ]
    )
    s3_lambda >> outputs_dal
