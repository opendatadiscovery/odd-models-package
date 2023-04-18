"""
For that example ODD_PLATFORM_HOST and ODD_PLATFORM_TOKEN environment variables must be set.

export ODD_PLATFORM_HOST="http://localhost:8080"
export ODD_PLATFORM_TOKEN=*ODD_PLATFORM_TOKEN can be obtained from the OpenDataDiscovery platform UI.*

This example shows how to use the DataSource class to manual discovery for AWS.
The DataSource takes an ODDRN uniquely defines source for all data assets that are added to it.

The DataSource class is a context manager for the discovery process. All assets that are added to the DataSource will be
ingested into the ODD platform (using variables above) when the context is closed.

In that example we create a DataSource for AWS and add a Lambda function to it with one input and list of outputs.
"""

from odd_models.discovery import DataSource
from odd_models.discovery.data_assets import AWSLambda, S3Artifact
from odd_models.discovery.data_assets.data_asset_list import DataAssetsList

with DataSource("//cloud/aws/dev") as data_source:
    validation_lambda = AWSLambda.from_params(
        region="eu-central-1", account="0123456789", function_name="validation"
    )
    input_artifact = S3Artifact.from_url("s3://bucket/folder/test_data.csv")

    results = S3Artifact.from_url("s3://bucket/folder/test_result.csv")
    metrics = S3Artifact.from_url("s3://bucket/folder/test_metrics.json")

    input_artifact >> validation_lambda >> DataAssetsList([results, metrics])

    data_source.add_data_asset(validation_lambda)
