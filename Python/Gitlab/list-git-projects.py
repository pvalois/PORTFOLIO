#!/usr/bin/env python3

from gitlab import *
from dumper import dump
import json,sys,os
from pprint import pprint
from lib.credentials import *

(git_server,git_token)=get_token("server")

gl = Gitlab(git_server,oauth_token=git_token)

for group in gl.groups.list():
  for projects in group.projects.list():
    project = gl.projects.get(projects.id)
    print(f"git clone {project.http_url_to_repo}")



