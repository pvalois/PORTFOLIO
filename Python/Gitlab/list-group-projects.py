#!/usr/bin/env python3


from gitlab import *
import json
import requests
from lib.credentials import *

(git_server,git_token)=get_token("server")
gl = Gitlab(git_server,private_token=git_token)
final_result = []

def dump(url):
  head = {'Authorization' : 'Bearer '+git_token}
  try:
    r = requests.get(url, headers=head)
    objs=r.json()
  except:
    objs=[]

  for obj in objs:
    url=f'{git_server}/api/v4/projects/{project.id}/registry/repositories/{obj["id"]}'
    datas=requests.get(url, headers=head).json()
    yield(obj["id"],url,datas)


for group in gl.groups.list():
    for project in group.projects.list():
        url=f"{git_server}/api/v4/projects/{project.id}/registry/repositories/"
        project_entry = {
            "project_id": project.id,
            "project_name": project.name,
            "url": url,
            "datas": []
        }

        try:
            for repo_id, data in dump(url):
                project_entry["datas"].append(data)
        except Exception as e:
            print(f"Erreur sur {project.name}: {e}")

        final_result.append(project_entry)

# Convertir en JSON
json_output = json.dumps(final_result, indent=2, ensure_ascii=False)
print(json_output)


