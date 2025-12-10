#!/usr/bin/env python3 

from grafana_api.grafana_face import GrafanaFace

import json
import requests
import os
import configparser

config=configparser.ConfigParser()
config.read('credentials.ini')
cred=config['dockerized']

HOST=cred["hostname"]+":"+cred["port"]
TOKEN=cred["apikey"]

#grafana_api = GrafanaFace(auth=apikey, host=hostname+":"+port)
grafana_api = GrafanaFace(auth=TOKEN, host=HOST)

def get_dashboard(grafana,uid):
    url = grafana + "/api/dashboards/uid/{0}".format(uid)
    HTTP_GET_HEADERS = {'Authorization': 'Bearer ' + TOKEN}
    r = requests.get(url, headers=HTTP_GET_HEADERS, verify=False)
    return (r.status_code, r.content)


print ("Dashboards");
print ("-"*40)

for dash in grafana_api.search.search_dashboards():
  uid=dash["uid"]
  uri=dash["uri"]
  (status,content)=get_dashboard("http://"+HOST,uid)
  print ("  + %s %dKo" %(uri,len(content)/1024))
  output=os.path.join("dumps/dashboards/",uri+".json")
  path=os.path.dirname(output)

  os.makedirs(path, exist_ok=True)

  with open(output,"w") as f:
    print (json.dumps(json.loads(content.decode("utf8")), indent=2), file=f)

print ("")


