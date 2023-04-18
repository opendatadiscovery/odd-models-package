from odd_models.discovery.data_assets import AWSLambda, S3Artifact
from odd_models.discovery.data_assets.data_asset_list import DataAssetsList
from odd_models.discovery.helper import link_nodes


def test_link_nodes():
    artifact = S3Artifact.from_url("s3://bucket/inputs/key_one")
    s3_lambda = AWSLambda("transformer", "//aws/lambda/transformer")

    link_nodes(artifact, s3_lambda)
    assert len(s3_lambda.upstream) == 1
    link_nodes(s3_lambda, S3Artifact.from_url("s3://bucket/outputs/key_one"))
    assert len(s3_lambda.downstream) == 1


def test_link_nodes_with_list():
    s3_lambda = AWSLambda("transformer", "//aws/lambda/transformer")

    link_nodes(
        DataAssetsList(
            [
                S3Artifact.from_url("s3://bucket/inputs/key_one"),
                S3Artifact.from_url("s3://bucket/inputs/key_two"),
            ]
        ),
        s3_lambda,
    )
    assert len(s3_lambda.upstream) == 2

    link_nodes(
        s3_lambda,
        DataAssetsList(
            [
                S3Artifact.from_url("s3://bucket/outputs/key_one"),
                S3Artifact.from_url("s3://bucket/outputs/key_two"),
            ]
        ),
    )
    assert len(s3_lambda.downstream) == 2


def test_link_two_lambda():
    lambda_one = AWSLambda("transformer_one", "//aws/lambda/transformer_one")
    lambda_two = AWSLambda("transformer_two", "//aws/lambda/transformer_two")

    link_nodes(lambda_one, lambda_two)
    assert len(lambda_one.downstream) == 1
    assert len(lambda_two.upstream) == 1


def test_link_two_data_asset_lists():
    list_one = DataAssetsList(
        [
            AWSLambda("transformer_one", "//aws/lambda/transformer_one"),
            AWSLambda("transformer_two", "//aws/lambda/transformer_two"),
        ]
    )
    list_two = DataAssetsList(
        [
            AWSLambda("transformer_two", "//aws/lambda/transformer_three"),
            AWSLambda("transformer_two", "//aws/lambda/transformer_four"),
        ]
    )

    link_nodes(list_one, list_two)
    assert len(list_one[0].upstream) == 0
    assert len(list_one[0].downstream) == 2

    assert len(list_one[1].upstream) == 0
    assert len(list_one[1].downstream) == 2

    assert len(list_two[0].upstream) == 2
    assert len(list_two[0].downstream) == 0
    assert len(list_two[1].upstream) == 2
    assert len(list_two[1].downstream) == 0
