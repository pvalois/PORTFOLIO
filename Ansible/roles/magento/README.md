Role Name
=========

Magento E-Commerce installation reole

Requirements
------------

MariaDb et Nginx must be installed

Role Variables
--------------

See *defaults/main.yml*

Dependencies
------------

None

Example Playbook
----------------

```yaml
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
```

License
-------

BSD

Author Information
------------------

Written for an ansible course, on *Superprof* E-learning platform. 
