#!/usr/bin/env python3

from aws_local import client

dynamodb = client("dynamodb")

table_name = "test_table"

# Créer table
try:
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )
    print(f"Table '{table_name}' créée")
except Exception as e:
    print(f"Erreur création table: {e}")

# Insérer un item
dynamodb.put_item(TableName=table_name, Item={"id": {"S": "1"}, "value": {"S": "Hello"}})
print("Item inséré")

# Lire un item
resp = dynamodb.get_item(TableName=table_name, Key={"id": {"S": "1"}})
print("Item lu:", resp.get("Item"))

