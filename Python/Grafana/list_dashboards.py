#!/usr/bin/env python3 

from grafana_api.grafana_face import GrafanaFace
import json
import configparser

config=configparser.ConfigParser()
config.read('credentials.ini')
cred=config['dockerized']

hostname=cred["hostname"]
port=cred["port"]
apikey=cred["apikey"]

grafana_api = GrafanaFace(auth=apikey,
                          host=hostname+":"+port)

print (json.dumps(grafana_api.search.search_dashboards(),indent=2))

try:
  print (json.dumps(grafana_api.search.search_datasources(),indent=2))
except:
  pass
