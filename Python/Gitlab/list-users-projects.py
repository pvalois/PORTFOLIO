#!/usr/bin/env python3

from gitlab import *
from dumper import dump
import json,sys,os
from pprint import pprint
from lib.credentials import *

(git_server,git_token)=get_token("tek")

gl = Gitlab(git_server,oauth_token=git_token)

users = gl.users.list(all=True)

for user in users:
    try:
        projects = user.projects.list(all=True)
        for project in projects:
            print(f"git clone {project.http_url_to_repo}")
    except Exception as e:
        print(f"# Impossible d'accéder aux projets de {user.username}: {e}")


