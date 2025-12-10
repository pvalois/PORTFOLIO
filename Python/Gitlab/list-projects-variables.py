#!/usr/bin/env python3


from gitlab import *
from lib.credentials import *
import json,requests
from rich.table import Table,box
from rich.console import Console

(git_server,git_token)=get_token("server")
gl = Gitlab(git_server,private_token=git_token)

def get_variables(url):
  head = {'Authorization' : 'Bearer '+git_token}
  r = requests.get(url, headers=head)
  obj=r.json()

  if (len(obj)>0): 
    for sobj in obj: yield(sobj['key'])


table = Table(box=box.MINIMAL)

table.add_column("Level", style="cyan")
table.add_column("ID", style="white")
table.add_column("Name", style="white")
table.add_column("Variables", style="yellow")

for group in gl.groups.list():
  variables = list(get_variables(git_server+"/api/v4/groups/"+str(group.id)+"/variables"))
  table.add_row("Group Level",str(group.id),group.name,"\n".join(variables))

  for project in group.projects.list():
    variables = list(get_variables(git_server+"/api/v4/projects/"+str(project.id)+"/variables"))
    table.add_row("  Project Level",f"{group.id}:{project.id}",project.name,"\n".join(variables))

console=Console()
console.print(table)

