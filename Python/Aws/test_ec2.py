#!/usr/bin/env python3 

import boto3
from botocore.client import Config
from aws_local import client
from pprint import pprint

ec2 = client("ec2")

# Créer une instance de test
ec2.run_instances(
    ImageId="ami-test",      # LocalStack accepte n'importe quelle string
    InstanceType="t2.micro",
    MinCount=1,
    MaxCount=1
)

# Vérifier la liste des instances
response = ec2.describe_instances()
pprint(response)

