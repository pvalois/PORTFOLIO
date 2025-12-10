#!/usr/bin/env python3

from aws_local import client

services = ["ecs", "s3", "lambda", "sqs", "sns", "dynamodb", "apigateway"]

for svc in services:
    c = client(svc)
    print(f"{svc}: {c.list_buckets() if svc=='s3' else c}")

