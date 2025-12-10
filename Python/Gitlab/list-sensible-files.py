#!/usr/bin/env python3

import json, sys, re
from gitlab import *
from lib.credentials import *
from rich.table import Table,box
from rich.console import Console

(git_server,git_token)=get_token("server")
gl = Gitlab(git_server,oauth_token=git_token)

table = Table(box=box.MINIMAL)

table.add_column("Project Name", style="cyan")
table.add_column("Filename", style="white")
table.add_column("Line", style="white")
table.add_column("Words", style="white")

banned_words = ["password", "secret", "token", "key", "pass"]

def get_project_files(project):
  for obj in project.repository_tree():
     yield(obj["path"])

for group in gl.groups.list():
    for projects in group.projects.list():
        project = gl.projects.get(projects.id)
        files=list(get_project_files(project))
        for file in files:
            if (file==".gitignore"): continue
            try:
              ide = [d['id'] for d in project.repository_tree() if d['name'] == file][0]
              file_content = project.repository_raw_blob(ide).decode("UTF-8")
            except:
              continue

            for lineno, line in enumerate(file_content.splitlines(), start=1):
                line = line.strip('\r').lower()
                if any(word in line.lower() for word in banned_words):
                    table.add_row(project.name, file, f"{lineno:-5}: {line}")

console=Console()
console.print(table)

