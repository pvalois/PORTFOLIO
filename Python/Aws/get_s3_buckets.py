#!/usr/bin/env python3
import os
import boto3
from aws_local import client

s3 = client("s3")

buckets = s3.list_buckets()
for b in buckets.get("Buckets", []):
    print(b["Name"])
