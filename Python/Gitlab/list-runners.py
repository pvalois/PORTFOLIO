#!/usr/bin/env python3


from gitlab import *
from lib.credentials import *
from rich.table import Table, box
from rich.console import Console

table = Table(title="Population test")

(git_server,git_token)=get_token("server")
gl = Gitlab(git_server,oauth_token=git_token)


table = Table(box=box.MINIMAL,show_lines=False)

table.add_column("ID", style="cyan")
table.add_column("Description", style="white")
table.add_column("IP", style="white")
table.add_column("Status", style="white")

for runner in gl.runners.all():
    table.add_row(str(runner.id), runner.description, runner.ip_address,  runner.status);

console=Console()
console.print(table)
    
