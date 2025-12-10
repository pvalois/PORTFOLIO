#!/usr/bin/env python3 

import boto3
from botocore.client import Config
from configlocator import *

# Chargement de la configuration depuis aws.ini
config = configlocator("aws.ini")
c = config["pepiniere"]

endpoint = c["endpoint"]
access_key = c["access_key_id"]
secret = c["access_key_secret"]
region = c["region"]

ec2 = boto3.client(
        "ec2",
        endpoint_url=endpoint,               # LocalStack
        aws_access_key_id=access_key,
        aws_secret_access_key=secret,
        region_name=region,
        config=Config(signature_version="v4") # important pour EC2
)


for i in ec2.instances.all():
    if i.state['Name'] == 'stopped':
        i.start()





