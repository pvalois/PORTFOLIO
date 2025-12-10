#!/usr/bin/env python3

from aws_local import client
import zipfile
import io

lambda_client = client("lambda")

# Préparer un package lambda simple
func_code = """
def handler(event, context):
    return {"message": "Hello LocalStack!"}
"""

zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, 'w') as zf:
    zf.writestr("lambda_function.py", func_code)
zip_buffer.seek(0)

func_name = "test_lambda"

try:
    lambda_client.create_function(
        FunctionName=func_name,
        Runtime="python3.12",
        Role="arn:aws:iam::000000000000:role/lambda-role",
        Handler="lambda_function.handler",
        Code={"ZipFile": zip_buffer.read()},
        Publish=True
    )
    print(f"Lambda '{func_name}' créée")
except Exception as e:
    print(f"Erreur création Lambda: {e}")

# Appeler la Lambda
response = lambda_client.invoke(FunctionName=func_name)
print("Invocation Lambda:", response["Payload"].read().decode())

