## Prestahop installation 

Requirements
------------

Role Variables
--------------

There is a lot of customisable things, like : 

* Prestahop version 
* Your domain 
* The database host (passwords **should* be crypted by **vault**)
* The language 
* The admin account (passwords **should* be crypted by **vault**)

See *defaults/main.yml*.

Dependencies
------------

Requires my mariadb and nginx roles presents

Example Playbook
----------------

```yaml
- name: Install

  hosts:
    - your_target 

  tasks:
    - name: Install Mariadb
      ansible.builtin.import_role:
        name: mariadb
      delegate_to: "{{ prestashop_db_server | regex_replace('localhost', ansible_hostname) }}"

    - name: Install Nginx
      ansible.builtin.import_role:
        name: nginx

    - name: Install Prestashop
      ansible.builtin.include_role:
        name: prestashop
```

License
-------

BSD

Author Information
------------------

Pascal Valois
