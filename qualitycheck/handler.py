import os
import json

from qualitycheck.awslambda import AwsLambda
from qualitycheck.utils import send_email_message


def data_quality_check_handler(event, context):
    """Check the data. If the measured value is identified
    as aberrant, invoke the notification Lambda function
    to send a notification lab technicians.
    """
    aws_region = os.environ['AWS_REGION']
    notifier_lambda = os.environ['NOTIFIER_LAMBDA_ARN']
    record = event['Records'][0]
    body = json.loads(record['body'])
    sample_id = body['sampleId']

    measured_value = float(body['absorbanceResult'])
    problem_detected = False
    msg = None

    if measured_value >= 1:
        msg = f'Absorbance for {sample_id} exceeds 1. Consider diluting the sample.'
        problem_detected = True
    elif not 0 < measured_value < 0.67:
        msg = f'Absorbance for {sample_id} with a measured value of ' \
              f'{measured_value} does not fall within the calibration curve'
        problem_detected = True
    else:
        pass

    if problem_detected and msg is not None:
        aws_lambda = AwsLambda(region=aws_region)
        payload = {
            'sampleId': sample_id,
            'message': msg
        }
        try:
            aws_lambda.invoke(
                function_name=notifier_lambda,
                payload=payload
            )
        except Exception:
            pass


def problem_notification_handler(event, context):
    """Send a notification using a self-managed SMTP
    server.
    """
    smtp_server_host = os.environ['SMTP_SERVER']

    sample_id = event['sampleId']
    message = event['message']

    send_email_message(
        message=message,
        subject=f'Data Quality Issue for {sample_id}',
        email_from='automated-checks@fake.gov',
        email_to='lab-tech-group@fake.gov',
        smtp_server=smtp_server_host
    )
