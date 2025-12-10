#!/usr/bin/env python3

from aws_local import client

sqs = client("sqs")

queue_name = "test-queue"

# Créer une queue
url = sqs.create_queue(QueueName=queue_name)["QueueUrl"]
print("Queue créée:", url)

# Envoyer un message
sqs.send_message(QueueUrl=url, MessageBody="Hello SQS")
print("Message envoyé")

# Lire les messages
messages = sqs.receive_message(QueueUrl=url, MaxNumberOfMessages=10).get("Messages", [])
for msg in messages:
    print("Message reçu:", msg["Body"])

