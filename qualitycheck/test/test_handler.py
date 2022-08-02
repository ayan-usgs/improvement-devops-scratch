import json

from unittest import mock

import pytest

from qualitycheck.handler import data_quality_check_handler, problem_notification_handler


@pytest.fixture
def okay_data():
    return {'sampleId': '7030d623-cdfc-41ba-a39f-b43aac54193c', 'absorbanceResult': '0.45'}


@pytest.fixture
def high_abs_data(okay_data):
    okay_data['absorbanceResult'] = '2.3'
    return okay_data


@pytest.fixture
def beyond_calibration_data(okay_data):
    okay_data['absorbanceResult'] = '0.94'
    return okay_data


@mock.patch.dict('os.environ', {'AWS_REGION': 'us-south-94', 'NOTIFIER_LAMBDA_ARN': 'aws:arn:us-south-94:my-lambda'})
@mock.patch('qualitycheck.handler.AwsLambda')
def test_okay_data(mock_awslambda, okay_data):
    event = {'Records': [{'body': json.dumps(okay_data)}]}
    context = {}

    data_quality_check_handler(event, context)
    mock_awslambda.assert_not_called()


@mock.patch.dict('os.environ', {'AWS_REGION': 'us-south-94', 'NOTIFIER_LAMBDA_ARN': 'aws:arn:us-south-94:my-lambda'})
@mock.patch('qualitycheck.handler.AwsLambda')
def test_high_data(mock_awslambda, high_abs_data):
    al = mock.Mock()
    mock_awslambda.return_value = al
    event = {'Records': [{'body': json.dumps(high_abs_data)}]}
    context = {}

    data_quality_check_handler(event, context)
    al.invoke.assert_called_with(
        function_name='aws:arn:us-south-94:my-lambda',
        payload={
            'sampleId': '7030d623-cdfc-41ba-a39f-b43aac54193c',
            'message': 'Absorbance for 7030d623-cdfc-41ba-a39f-b43aac54193c exceeds 1. Consider diluting the sample.'
        }
    )


@mock.patch.dict('os.environ', {'AWS_REGION': 'us-south-94', 'NOTIFIER_LAMBDA_ARN': 'aws:arn:us-south-94:my-lambda'})
@mock.patch('qualitycheck.handler.AwsLambda')
def test_beyond_calibration_data(mock_awslambda, beyond_calibration_data):
    al = mock.Mock()
    mock_awslambda.return_value = al
    event = {'Records': [{'body': json.dumps(beyond_calibration_data)}]}
    context = {}

    data_quality_check_handler(event, context)
    al.invoke.assert_called_with(
        function_name='aws:arn:us-south-94:my-lambda',
        payload={
            'sampleId': '7030d623-cdfc-41ba-a39f-b43aac54193c',
            'message': 'Absorbance for 7030d623-cdfc-41ba-a39f-b43aac54193c with a measured value of 0.94 does not fall within the calibration curve'
        }
    )


@pytest.fixture
def notification_event():
    event = {
        'sampleId': '7030d623-cdfc-41ba-a39f-b43aac54193c',
        'message': 'Absorbance for 7030d623-cdfc-41ba-a39f-b43aac54193c exceeds 1. Consider diluting the sample.'
    }
    return event


@mock.patch.dict('os.environ', {'SMTP_SERVER': 'some-smtp-server.fake.gov'})
@mock.patch('qualitycheck.handler.send_email_message')
def test_problem_notification_handler(mock_sem, notification_event):
    problem_notification_handler(notification_event, {})
    mock_sem.assert_called_with(
        message='Absorbance for 7030d623-cdfc-41ba-a39f-b43aac54193c exceeds 1. Consider diluting the sample.',
        subject='Data Quality Issue for 7030d623-cdfc-41ba-a39f-b43aac54193c',
        email_from='automated-checks@fake.gov',
        email_to='lab-tech-group@fake.gov',
        smtp_server='some-smtp-server.fake.gov'
    )