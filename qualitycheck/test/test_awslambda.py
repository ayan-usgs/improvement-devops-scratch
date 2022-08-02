import json
from unittest import mock

import pytest

from qualitycheck.awslambda import AwsLambda


@pytest.fixture
def params():
    region = 'us-south-94'
    function = 'arn:aws:lambda:my-function'
    payload = {'spam': 'eggs'}
    return region, function, payload


@mock.patch('qualitycheck.awslambda.boto3.client')
def test_client_create(m_client, params):
    region, _, _ = params
    AwsLambda(region=region)
    m_client.assert_called_with('lambda', region_name=region)


@mock.patch('qualitycheck.awslambda.boto3.client')
def test_invoke(m_client, params):
    region, function, payload = params
    al = AwsLambda(region=region)
    al.invoke(
        function_name=function,
        payload=payload
    )
    m_client.return_value.invoke_assert_called_with(
        FunctionName=function,
        Payload=json.dumps(payload).encode(),
        InvocationType='RequestResponse'
    )
