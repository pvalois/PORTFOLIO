#!/usr/bin/env python3

import sys
import requests
from gitlab import *
from lib.credentials import *

(GITLAB_URL,PRIVATE_TOKEN)=get_token("server")
print (GITLAB_URL)

try: 
  PROJECT_ID = sys.argv[1]
except:
  print (f"Usage : {sys.argv[0]} <project_id>")
  sys.exit(0)

headers = {
    "PRIVATE-TOKEN": PRIVATE_TOKEN
}

def get_variables():
    url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/variables"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def mask_variable(var):
    url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/variables/{var['key']}"
    payload = {
        "value": var['value'],  # obligatoire sinon GitLab crache
        "variable_type": var['variable_type'],
        "environment_scope": var['environment_scope'],
        "masked": True,
    }
    response = requests.put(url, headers=headers, data=payload)
    if response.status_code == 200:
        print(f"✅ Masqué : {var['key']}")
    else:
        print(f"❌ Échec : {var['key']} ({response.status_code})")

for var in get_variables():
  value = var.get("value", "")
  if (8 <= len(value) <= 100 and all(c.isalnum() or c in "_+=/@:.-" for c in value)):
    mask_variable(var)
  else:
    print(f"⚠️  Ne peut pas être masquée (invalide) : {var['key']}")

