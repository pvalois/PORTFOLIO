#!/usr/bin/env python3

import boto3
from botocore.client import Config
from configlocator import *
from pprint import pprint

# Chargement de la configuration depuis aws.ini
config = configlocator("aws.ini")
c = config["pepiniere"]

endpoint = c["endpoint"]
access_key = c["access_key_id"]
secret = c["access_key_secret"]
region = c["region"]


def get_instances():
    """
    Retourne la liste des instances EC2 visibles sur l'endpoint configuré.
    """
    ec2 = boto3.client(
        "ec2",
        endpoint_url=endpoint,               # LocalStack
        aws_access_key_id=access_key,
        aws_secret_access_key=secret,
        region_name=region,
        config=Config(signature_version="v4") # important pour EC2
    )

    try:
        response = ec2.describe_instances()
    except Exception as e:
        print(f"Erreur describe_instances : {e}")
        return []

    instances = []

    for reservation in response.get("Reservations", []):
        for inst in reservation.get("Instances", []):

            # Récupération du tag "Name"
            name = "N/A"
            for tag in inst.get("Tags", []):
                if tag.get("Key") == "Name":
                    name = tag.get("Value")
                    break

            instances.append({
                "InstanceId": inst.get("InstanceId"),
                "Name": name,
                "Type": inst.get("InstanceType"),
                "State": inst.get("State", {}).get("Name"),
                "PrivateIP": inst.get("PrivateIpAddress"),
                "PublicIP": inst.get("PublicIpAddress"),
                "LaunchTime": inst.get("LaunchTime")
            })

    return instances


# Exemple d'utilisation
if __name__ == "__main__":
    for inst in get_instances():
        pprint(inst)

