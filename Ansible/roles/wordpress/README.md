## Wordpress installation 

This role will : 

* Install Wordpress
* Set admin account
* Install wordpress cli and create first page
* Add a nginx front (ssl not included)

Requirements
------------

Role Variables
--------------

There is a lot of customisable things, like : 

* Your domain 
* The database host (passwords **should* be crypted by **vault**)
* The admin account (passwords **should* be crypted by **vault**)
* The title of your site

See *defaults/main.yml*.

Dependencies
------------

Requires my mariadb and nginx roles presents

Example Playbook
----------------

```yaml
- name: Install Wordpress

  hosts:
    - your_target

  tasks:

    - name: Install Prequesites
      ansible.builtin.include_role:
        name: wordpress
        tasks_from: prequesites.yml

    - name: Install mariadb
      ansible.builtin.import_role:
        name: mariadb
      delegate_to: "{{ wordpress_mysql_host | regex_replace('localhost', ansible_hostname) }}"

    - name: Install nginx
      ansible.builtin.include_role:
        name: nginx

    - name: Setup Database
      ansible.builtin.import_role:
        name: wordpress
        tasks_from: setup_database.yml
      delegate_to: "{{ wordpress_mysql_host | regex_replace('localhost', ansible_hostname) }}"

    - name: Download and Install
      ansible.builtin.include_role:
        name: wordpress
        tasks_from: download_and_extract_wordpress.yml

    - name: Setup Wordpress
      ansible.builtin.include_role:
        name: wordpress
        tasks_from: setup_wordpress.yml

    - name: Setup http server
      ansible.builtin.include_role:
        name: wordpress
        tasks_from: setup_and_restart_http_server.yml
```

License
-------

BSD

Author Information
------------------

Pascal Valois
