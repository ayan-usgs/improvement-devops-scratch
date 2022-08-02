import json

import boto3


class AwsLambda:

    def __init__(self, region='us-west-2'):
        self.region = region
        self.client = boto3.client('lambda', region_name=self.region)

    def invoke(self, function_name, payload, invocation_type='RequestResponse'):
        resp = self.client.invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            Payload=json.dumps(payload).encode()
        )
        return resp
