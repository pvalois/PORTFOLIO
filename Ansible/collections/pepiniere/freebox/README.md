# Ansible Collection - pepiniere.freebox

A sample colletion to demonstrate **plugin writing for ansible**,
based on **freebox** dhcp lease administration

Example: 

```yaml
- name: Lister les leases DHCP sur Freebox

  hosts: localhost

  gather_facts: false

  tasks:
    - name: Récupérer les leases DHCP
      pepiniere.freebox.list_dhcp:
        api_url: "VAULT_REDACTED"
        filter_status: online
      register: dhcp_leases

    - name: Récupérer les IP reachables de teknomage
      set_fact:
        teknomage_ips: >-
          {{
            dhcp_leases.leases
            | selectattr('default_name', 'equalto', 'teknomage')
            | map(attribute='l3connectivities')
            | map('selectattr', 'reachable', 'equalto', True)
            | map('map', attribute='addr')
            | map('list')
            | list
            | flatten
          }}

    - name: Afficher le résultat
      debug:
        var: teknomage_ips

    - name: Générer dictionnaire hostname -> IP reachables
      set_fact:
        reachable_ips_by_host: >-
          {{
            dict(
              dhcp_leases.leases
              | map(
                  attribute='default_name'
                )
              | zip(
                  dhcp_leases.leases
                  | map(attribute='l3connectivities')
                  | map('selectattr', 'reachable', 'equalto', True)
                  | map('map', attribute='addr')
                  | map('list')
                )
            )
          }}

    - name: Afficher le résultat
      debug: 
        var: reachable_ips_by_host

    - name: Affecter une lease statique 
      pepiniere.freebox.static_lease:
        api_url: "VAULT_REDACTED"
        api_token: "VAULT_REDACTED"
        client_name: xencloak
        client_mac_address: "BC:24:11:04:DB:D4"
        client_ip: 192.168.1.218
``` 

Usage: 

```bash
make build
make install 
make check
make check-doc

# OR 

make all
```
