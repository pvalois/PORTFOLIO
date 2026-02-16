#!/usr/bin/env python3

import boto3
from botocore.client import Config
from pprint import pprint
from aws_local import client



def get_instances():
    """
    Retourne la liste des instances EC2 visibles sur l'endpoint configuré.
    """
    ec2 = client("ec2")

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

