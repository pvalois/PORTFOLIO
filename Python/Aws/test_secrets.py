#!/usr/bin/env python3

from aws_local import client

secrets = client("secretsmanager")

secret_name = "test-secret"

try:
    secrets.create_secret(Name=secret_name, SecretString="mysecret123")
    print(f"Secret '{secret_name}' créé")
except Exception as e:
    print(f"Erreur création secret: {e}")

# Lire le secret
resp = secrets.get_secret_value(SecretId=secret_name)
print("Secret lu:", resp.get("SecretString"))

