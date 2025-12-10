#!/usr/bin/env python3
import time
import botocore
from aws_local import client
from rich.table import Table, box
from rich.console import Console
import humanize

console = Console()
s3 = client("s3")

bucket_name = "mon-bucket-test"

def bucket_exists(name):
    try:
        s3.head_bucket(Bucket=name)
        return True
    except botocore.exceptions.ClientError as e:
        code = e.response.get("Error", {}).get("Code", "")
        if code in ("404", "NoSuchBucket", "NotFound"):
            return False
        # d'autres erreurs -> remonter
        raise

def wait_for_bucket(name, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        if bucket_exists(name):
            return True
        time.sleep(0.5)
    return False

# 1) Création du bucket (robuste vis-à-vis de la région)
try:
    region = getattr(s3.meta, "region_name", None)
except Exception:
    region = None

created = False
try:
    if region in (None, "", "us-east-1"):
        # us-east-1 : ne pas fournir LocationConstraint
        s3.create_bucket(Bucket=bucket_name)
    else:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": region}
        )
    created = True
    print(f"Bucket '{bucket_name}' : create_bucket() success.")
except botocore.exceptions.ClientError as e:
    errcode = e.response.get("Error", {}).get("Code", "")
    errmsg = e.response.get("Error", {}).get("Message", str(e))
    # Cas fréquent : LocationConstraint incompatible -> retenter sans config
    if errcode in ("IllegalLocationConstraintException",):
        try:
            s3.create_bucket(Bucket=bucket_name)
            created = True
            print(f"Bucket '{bucket_name}' créé (retry sans LocationConstraint).")
        except botocore.exceptions.ClientError as e2:
            err2 = e2.response.get("Error", {}).get("Code", "")
            if err2 in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
                print(f"Bucket '{bucket_name}' existe déjà (owned).")
                created = True
            else:
                print(f"Erreur création bucket (retry): {e2}")
                raise
    elif errcode in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
        print(f"Bucket '{bucket_name}' existe déjà (owned).")
        created = True
    else:
        print(f"Erreur création bucket: {errcode} - {errmsg}")
        raise

# 2) S'assurer que le bucket est accessible avant upload
if not created:
    print("Le bucket n'a pas pu être créé. Abandon.")
    raise SystemExit(1)

if not wait_for_bucket(bucket_name, timeout=15):
    print(f"Le bucket '{bucket_name}' n'est pas joignable après attente. Abandon.")
    raise SystemExit(1)

# 3) Upload d'un objet test (avec gestion d'erreur si bucket introuvable)
key = "hello.txt"
body = b"Hello LocalStack / AWS!"

try:
    s3.put_object(Bucket=bucket_name, Key=key, Body=body)
    print(f"Objet '{key}' uploadé dans '{bucket_name}'.")
except botocore.exceptions.ClientError as e:
    errcode = e.response.get("Error", {}).get("Code", "")
    print(f"Erreur upload objet: {errcode} - {e}")
    # Si NoSuchBucket malgré tout -> afficher buckets existants
    if errcode in ("NoSuchBucket", "404", "NotFound"):
        print("Liste des buckets connus :")
        try:
            for b in s3.list_buckets().get("Buckets", []):
                print(" -", b["Name"])
        except Exception:
            pass
    raise
