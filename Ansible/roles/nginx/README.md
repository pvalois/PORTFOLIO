## Role to install nginx web server

This role provides : 

* Include variables to customize installation (see *defaults/main.yml*, and *host_vars*)
* Includes dynamic VirtualHost configuration and a customizable landing page via Jinja2 templates. 
* Provide static default html home page
* Debian and RedHat compliance due to *OS family* specific variable files


