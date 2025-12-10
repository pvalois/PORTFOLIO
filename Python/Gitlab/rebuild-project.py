#!/usr/bin/env python3


from dumper import dump
import json
import sys
from pprint import pprint
import requests
from gitlab import *
from lib.credentials import *
import datetime

(git_server,git_token)=get_token("server")
gl = Gitlab(git_server,private_token=git_token)

head = {'Authorization' : 'Bearer '+git_token,
        'Content-type': 'Application/json'}

ddate="Rebuild ordered on "+str(datetime.datetime.now())

payload={"branch": "main",
         "commit_message": "Rebuilding",
         "actions": [{"action": "update",
                      "file_path": "rebuild.log",
                      "content": ddate }]}

def post_file(projectid,payload):
  url=git_server+'/api/v4/projects/'+str(projectid)+'/repository/commits/'
  r = requests.post(url, headers=head, data=json.dumps(payload))
  obj=r.json()
  return(obj)

for group in gl.groups.list():
  for project in group.projects.list():
    print (">>  ",project.id,project.name)
    print (json.dumps(post_file(project.id,payload),indent=2))
      
