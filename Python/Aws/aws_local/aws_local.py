import boto3
from botocore.client import Config
from configlocator import *

config=configlocator("aws.ini")

c=config['pepiniere']
endpoint=c['endpoint']
access_key=c['access_key_id']
secret=c['access_key_secret']
region=c['region']


def client(service_name):
    """Retourne un client boto3 configuré pour LocalStack."""

    return boto3.client(
        service_name,
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret,
        region_name=region,
        config=Config(signature_version='v4')
    )
