#!/usr/bin/env python3


from gitlab import *
import sys
import time
import json
from lib.credentials import *
from rich.table import Table, box
from rich.console import Console

def chunked_join(lst, size=5):
    strs = [str(x.id) for x in lst]
    blocks = [",".join(strs[i:i+size]) for i in range(0, len(strs), size)]
    return ("\n".join(blocks))

(git_server,git_token)=get_token("server")
gl = Gitlab(git_server,oauth_token=git_token)

table = Table(box=box.MINIMAL)

table.add_column("RID", style="cyan")
table.add_column("Description", style="white")
table.add_column("RIPADDR", style="white")
table.add_column("Jobs ID", style="white")

for runner in gl.runners.all():
    table.add_row(str(runner.id), runner.description, runner.ip_address, chunked_join(runner.jobs.list()))

console=Console()
console.print(table)
