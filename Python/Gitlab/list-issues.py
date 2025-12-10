#!/usr/bin/env python3 

from gitlab import *
from lib.credentials import *
from rich.table import Table,box
from rich.console import Console

(git_server,git_token)=get_token("server")
gl = Gitlab(git_server,oauth_token=git_token)

table = Table(box=box.MINIMAL)

table.add_column("ID", style="cyan")
table.add_column("Title", style="cyan")
table.add_column("Created at")
table.add_column("Updated at")
table.add_column("Closed at")

issues = gl.issues.list()
for issue in issues:
  project = gl.projects.get(issue.project_id)
  munchable = project.issues.get(issue.iid)
  table.add_row(str(munchable.id),munchable.title,munchable.created_at,munchable.updated_at,munchable.closed_at)

console=Console()
console.print(table)
