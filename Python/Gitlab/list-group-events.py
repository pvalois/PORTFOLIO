#!/usr/bin/env python3


from gitlab import *
from lib.credentials import *
from rich.table import Table, box
from rich.console import Console


(git_server,git_token)=get_token("server")

gl = Gitlab(git_server,private_token=git_token)

table = Table(box=box.MINIMAL)

table.add_column("Group", style="cyan")
table.add_column("Project ID", style="white")
table.add_column("Project Name", style="white")
table.add_column("URL",style="yellow")

def get_projects(group):
  for project in group.projects.list():
    url=f"{git_server}/api/v4/projects/{project.id}/audit_events/"
    yield(project.id,project.name,url)


if __name__ == "__main__" :
    for group in gl.groups.list():
        projects=list(get_projects(group))
        uniqed=set([(pid, name) for pid, name, url in projects])
        for thisid, thisname in uniqed:
          urls=[url for pid, name, url in projects if pid==thisid]
          table.add_row(group.name,str(thisid),thisname,"\n".join(urls))

    console=Console()
    console.print(table)
