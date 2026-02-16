import boto3
from botocore.client import Config
from configlocator import *
import os

def get_custom_config(section=None):
    """Tente de charger la config depuis aws.ini."""
    try:
        # On cherche le fichier aws.ini
        config = configlocator("aws.ini")
        c = config[section]
        return {
            'endpoint_url': c.get('endpoint'),
            'aws_access_key_id': c.get('access_key_id'),
            'aws_secret_access_key': c.get('access_key_secret'),
            'region_name': c.get('region'),
        }
    except (FileNotFoundError, KeyError, Exception):
        # Si le fichier n'existe pas ou que la section 'pepiniere' est absente
        return {}

def client(service_name):
    custom_params = get_custom_config("pepiniere")

    # Si custom_params est vide, boto3 cherchera automatiquement 
    # dans ~/.aws/credentials ou les variables d'environnement.
    return boto3.client(
        service_name,
        config=Config(signature_version='v4'),
        **custom_params
    )
