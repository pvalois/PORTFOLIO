#!/usr/bin/env python3
import sys
import boto3
from botocore.client import Config
from configlocator import configlocator

def main():
    # Vérification argument
    if len(sys.argv) != 2:
        print("Usage: create-bucket.py <bucket-name>")
        sys.exit(1)

    bucket_name = sys.argv[1]

    # Lecture config
    config = configlocator("aws.ini")
    c = config['pepiniere']

    endpoint = c['endpoint']
    access_key = c['access_key_id']
    secret = c['access_key_secret']
    region = c['region']

    # Client S3
    s3 = boto3.client(
        's3',
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret,
        config=Config(signature_version='s3v4'),
        region_name=region
    )

    # Création du bucket
    try:
        # Certains backends S3 (ex: MinIO) n'ont pas besoin de LocationConstraint
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            # Essayer avec LocationConstraint si ce n'est pas AWS
            s3.create_bucket(
                Bucket=bucket_name,
                #CreateBucketConfiguration={
                #    'LocationConstraint': region
                #}
            )
        else:
            s3.create_bucket(Bucket=bucket_name)

        print(f"Bucket '{bucket_name}' créé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création du bucket : {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()

