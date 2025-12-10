#!/usr/bin/env python3 

from proxmoxer import ProxmoxAPI
import warnings
import sys
import configparser
import argparse
import json

warnings.filterwarnings("ignore")

config=configparser.ConfigParser()
config.read('/home/valois/.proxmox.ini')

creds=config['crucible']
server=creds["ip"]
user=creds["user"]
password=creds["password"]

prox = ProxmoxAPI(host=server, user=user, password=password, verify_ssl=False)
allv=prox.nodes("crucible").lxc.get()+prox.nodes("crucible").qemu.get()
labs=([c['name'] for c in allv if c['status'].lower()=='running'])

parser = argparse.ArgumentParser()
parser.add_argument('--list', action='store_true', help='List all hosts')
args = parser.parse_args()

if args.list: 
    print(json.dumps({
        "labs": {
            "hosts": labs
        },
        "_meta": {
            "hostvars": {}
        }
    }))
else:
    print("{}")

