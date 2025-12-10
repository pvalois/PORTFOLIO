#!/usr/bin/env python3 
#!/usr/bin/env python3

from gitlab import *
from lib.credentials import *
import requests
import json
import argparse

(git_server,git_token)=get_token("server")
gl = Gitlab(git_server,private_token=git_token)

parser = argparse.ArgumentParser( description="Liste et nettoie les artefacts des Jobs GitLab anciens.")
parser.add_argument( 'projects', type=str, help="Chemin des projets, séparés par des virgules.")
parser.add_argument('-b', '--branch', type=str, default="master", help="Chemin des projets, séparés par des virgules.")
args = parser.parse_args()

projects=args.projects.split(",")

for project in gl.projects.list():
  if ((project.path_with_namespace.lower() in projects) or len(projects)==0):
    print (f"Trigger pipeline for project {project.path_with_namespace}")
    url = f"{git_server}/api/v4/projects/{project.id}/pipeline"
    headers = {"PRIVATE-TOKEN": git_token}
    data = {"ref": args.branch}
    response = requests.post(url, headers=headers, data=data)
    print (json.dumps(response.json(), indent=2, ensure_ascii=False))

