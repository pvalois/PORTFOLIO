Role de provision virtual machines in proxmox : 

Playbook : 

- name: Provision vms

  hosts:
    - localhost

  tasks: 

  - name: Play proxmox_provision role
    ansible.builtin.include_role:
      name: proxmox_provision

Usage:  

  ansible-playbook playbook.yml -e @vars/profile.yaml

Where vars/profile.yaml describe vms to be create (samples provided).
