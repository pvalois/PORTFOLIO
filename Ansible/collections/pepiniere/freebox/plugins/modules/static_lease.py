#!/usr/bin/python3
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: my_custom_module
short_description: Module d'affectation dhcp statique
description:
  - Ce module permet de positionner un baille statique pour un client dhcp
options:
  api_url:
    description:
      - L'ip de la freebox
    required: true
    type: str
  api_token:
    description:
      - L'ip de la freebox
    required: true
    type: str
  client_name:
    description:
      - Le nom du client
    required: true
    type: str
  client_mac_address:
    description:
      - L'adresse mac du client
    required: true
    type: str
  client_ip:
    description:
      - L'ip a affecter
    required: true
    type: str
author:
  - Pascal Valois (pvalois@hotmail.fr)
'''



import json
import requests
from freepybox import Freepybox
from ansible.module_utils.basic import AnsibleModule

def get_dhcp_lease(api_url, client_name):

    fbx = Freepybox()
    fbx.open(api_url)
    devices = fbx.lan.get_hosts_list()

    for device in devices:
        if device.get('name') == client_name:
            return device  # Retourne la lease correspondante
    
    return None  # Si aucun device trouvé

def create_static_lease(api_base_url, token, client_name, client_mac, client_ip):
    url = f"http://{api_base_url}/api/v4/dhcp/static_lease/"

    payload = {
        "default_name": client_name,
        "mac": client_mac,
        "ip": client_ip
    }

    headers = {
        "X-Fbx-App-Auth": token,
        "Content-Type": "application/json"
    }

    resp = requests.post(url, json=payload, headers=headers, verify=False)
    resp.raise_for_status()
    data = resp.json()
    return data

def run_module():

    module_args = dict(
        api_url=dict(type='str', required=True),
        api_token=dict(type='str', required=True),
        client_name=dict(type='str', required=True),
        client_mac_address=dict(type='str', required=True),
        client_ip=dict(type='str', required=True)
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    api_url = module.params['api_url']
    api_token = module.params['api_token']
    client_name = module.params['client_name']
    client_mac_address = module.params['client_mac_address']
    client_ip = module.params['client_ip']

    try:
        lease = get_dhcp_lease(api_url, client_name)

        if lease:
            name_list = lease.get('name') or []
            source = name_list[0].get('source') if len(name_list) > 0 else None

            if source != 'dhcp': module.exit_json(changed=False)

            active_ips = [
                conn.get("addr")
                for conn in lease.get("l3connectivities") or []
                if conn.get("active") is True
            ]

            if client_ip in active_ips: module.exit_json(changed=False)

        response = create_static_lease(api_url, api_token, client_name, client_mac_address, client_ip)

        if response.get("success") is True:
            module.exit_json(changed=True, msg=f"Bail statique créé pour {client_name}", response=response)
        else:
            module.fail_json(msg=f"Échec de la création du bail statique pour {client_name}", response=response)

    except Exception as e:
        module.fail_json(msg=str(e))

def main():
    run_module()

if __name__ == '__main__':
    main()

