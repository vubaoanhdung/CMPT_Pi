import io
import json
import logging
import random
import time
import zipfile
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def invoke_lambda_function(lambda_client, function_name, function_params):
    """
    Invokes an AWS Lambda function.
    :param lambda_client: The Boto3 AWS Lambda client object.
    :param function_name: The name of the function to invoke.
    :param function_params: The parameters of the function as a dict. This dict
                            is serialized to JSON before it is sent to AWS Lambda.
    :return: The response from the function invocation.
    """
    print("Lambda invoked")
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            Payload=json.dumps(function_params).encode())
        logger.info("Invoked function %s.", function_name)
    except ClientError:
        logger.exception("Couldn't invoke function %s.", function_name)
        raise
    return response

lambda_client = boto3.client('lambda')
lambda_params = {
    "mode": "HEAT",
    "temperature": 21.5
}
lambda_function_name = 'changeThermostatSetting'

response = invoke_lambda_function(lambda_client, lambda_function_name, lambda_params)
print(json.load(response['Payload']))
        