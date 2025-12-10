#!/usr/bin/env python3


import sys, os, json, gitlab
from gitlab import *
from dumper import dump
from pprint import pprint
from lib.credentials import *

(git_server,git_token)=get_token("server")

def get_gitlab_ci(project):
  try:
    ide = [d['id'] for d in project.repository_tree() if d['name'] == '.gitlab-ci.yml'][0]
    file_content = project.repository_raw_blob(ide)
    return (file_content.decode("utf-8"))
  except:
    return ("")

def get_project_files(project):
  for obj in project.repository_tree():
    print ("    ", obj["path"])

gl = Gitlab(git_server,oauth_token=git_token)

for group in gl.groups.list():
  for projects in group.projects.list():
    project = gl.projects.get(projects.id)
    yaml=get_gitlab_ci(project)
    print (">> ",project.path_with_namespace)
    savepath='dump/'+project.path_with_namespace
    os.makedirs(savepath,exist_ok=True)
    f=open(savepath+"/gitlab-ci.yml","w")
    f.write(yaml)
    f.close()    


