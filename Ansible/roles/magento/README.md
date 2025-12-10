Role Name
=========

Installation d'une solution d'ecommerce basé sur magento. 

Requirements
------------

MariaDb et Nginx doivent être installés

Role Variables
--------------

mysql_root_password
server_hostname: ""
magento_dir
magento_www_group
magento_mode
magento_clean_old_install: False
magento_db_host
magento_db_name
magento_db_user
magento_db_password
magento_public_key
magento_private_key
base_url: http://yourdomain.co.uk/
use_rewrites: 1
language: en_GB
timezone: Europe/London
currency: GBP
backend_frontname: admin
admin_firstname
admin_lastname
admin_email
admin_user
admin_password

Dependencies
------------

None

Example Playbook
----------------

  tasks: 

  - name: Deploy Mysql
    ansible.builtin.import_role:
      name: mariadb-server
    
  - name: Deploy Nginx
    ansible.builtin.import_role:
      name: nginx
    
  - name: Deploy Magento
    ansible.builtin.import_role:
      name: magento

License
-------

BSD

Author Information
------------------

Ecrit dans le cadre d'un cours donné sur la plateforme Superprof, par Pascal Valois.
