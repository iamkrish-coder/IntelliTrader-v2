import boto3
import json

from backend.utils.logging_utils import *
from botocore.exceptions import ClientError


def get_secret(secret, region):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region
    )

    try:
        response = client.get_secret_value(SecretId=secret)
        secret_data = response['SecretString']
        log_info(f"Retrieving Secret Keys From AWS Secrets Manager ...COMPLETE!")
        return secret_data
    except ClientError as error:
        log_error(f"Error retrieving secret: {error}")
        raise error
