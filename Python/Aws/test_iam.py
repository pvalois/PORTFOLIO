#!/usr/bin/env python3

from aws_local import client

iam = client("iam")

role_name = "test-role"

try:
    role = iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument='{"Version": "2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
    )
    print(f"Role '{role_name}' créé")
except Exception as e:
    print(f"Erreur création role: {e}")

