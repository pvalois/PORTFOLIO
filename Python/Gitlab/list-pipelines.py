#!/usr/bin/env python3

from gitlab import *
from lib.credentials import *
from rich.table import Table, box
from rich.console import Console

(git_server,git_token)=get_token("server")
gl = Gitlab(git_server,private_token=git_token)

table = Table(box=box.MINIMAL)

table.add_column("Project", style="cyan")
table.add_column("Pipeline Url", style="white")
table.add_column("Pipeline Status", style="yellow")
table.add_column("Jobs", style="yellow")

for project in gl.projects.list():
  for pipeline in project.pipelines.list(all=True):
    jobs = project.jobs.list(pipeline_id=pipeline.id,all=True)
    joblist = [f"{j.id} {j.name} {j.status}" for j in jobs if j.pipeline['id'] == pipeline.id]

    color="[white]"
    if (pipeline.status=="running"): color="[cyan]"
    if (pipeline.status=="success"): color="[green]"
    if (pipeline.status=="failed"): color="[red]"
    table.add_row(project.name, pipeline.web_url, f"{color}{pipeline.status}", "\n".join(joblist)+"\n")

console=Console()
console.print(table)

