#!/usr/bin/env python3

import json, sys
from dumper import dump
from gitlab import *
from lib.credentials import *

(git_server,git_token)=get_token("server")
gl = Gitlab(git_server,private_token=git_token)

projects=["test"]

for project in gl.projects.list():
  if ((project.name.lower() in projects) or len(projects)==0):
    print ("*",project.name)

    pipelines=[x for x in project.pipelines.list()]

    for pipeline in pipelines:
      pipeline.delete()

     
    


