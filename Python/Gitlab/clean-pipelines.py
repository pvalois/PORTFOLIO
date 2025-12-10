#!/usr/bin/env python3

from gitlab import *
from lib.credentials import *
import argparse

(git_server,git_token)=get_token("server")
gl = Gitlab(git_server,private_token=git_token)

parser = argparse.ArgumentParser( description="Liste et nettoie les artefacts des Jobs GitLab anciens.")
parser.add_argument( 'projects', type=str, help="Chemin des projets, séparés par des virgules.")
args = parser.parse_args()

projects=args.projects.split(",")

status_to_delete=["failed","canceled","success"]

for project in gl.projects.list():
  if ((project.path_with_namespace.lower() in projects) or len(projects)==0):
    print ("*",project.path_with_namespace)
    for pipeline in project.pipelines.list()[0:]:
      if (pipeline.status in status_to_delete):
        print ("  ==> Deleting pipeline",pipeline.id)
        pipeline.delete()
    


