#!/usr/bin/python3
# -*- coding: utf-8 -*-

DOCUMENTATION = r'''
---
module: list_dhcp
short_description: Liste les leases DHCP
description: "Appelle l'API Freebox pour lister les leases DHCP"
options:
  api_url:
    description: "Adresse IP de la Freebox (ex: 192.168.1.254)"
    required: true
    type: str
  filter_status:
    description: "Filtre sur le status (None / online / offline / static)"
    required: false
    default: None
    type: bool
author: "Pascal Valois (pvalois@hotmail.fr)"
'''

EXAMPLES = r'''
- name: Récupérer toutes les leases DHCP
  pepiniere.freebox.dhcp_leases:
    api_url: 192.168.1.254
  register: result

- debug:
    var: result.leases
'''

RETURN = r'''
leases:
  description: Liste brute de toutes les leases DHCP
  type: list
  returned: always
'''

import json
from freepybox import Freepybox
from ansible.module_utils.basic import AnsibleModule

def get_dhcp_leases(api_url, filter_status=None):
    """
    Appelle l’API Freebox via freepybox et filtre les leases si demandé.

    filter_status: None / "online" / "offline" / "static"
    """
    fbx = Freepybox()
    fbx.open(api_url)
    devices = fbx.lan.get_hosts_list()

    if filter_status:
        if filter_status not in ['online', 'offline', 'static']:
            raise ValueError(f"filter_status invalide: {filter_status}")
        devices = [
            d for d in devices
            if (filter_status == 'online' and d['active']) or
               (filter_status == 'offline' and not d['active']) or
               (filter_status == 'static' and d['name'][0]['source']!='dhcp')
        ]

    return devices

def run_module():
    module_args = dict(
        api_url=dict(type='str', required=True),
        filter_status=dict(type='str', required=False, choices=['online','offline','static'])
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    api_url = module.params['api_url']
    filter_status = module.params.get('filter_status')

    try:
        leases = get_dhcp_leases(api_url, filter_status)
        module.exit_json(changed=False, leases=leases)

    except Exception as e:
        module.fail_json(msg=str(e))

def main():
    run_module()

if __name__ == '__main__':
    main()

