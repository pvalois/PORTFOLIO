#!/usr/bin/env python3

from gitlab import Gitlab
from lib.credentials import *
from rich.table import Table, box
from rich.console import Console

(git_server, git_token) = get_token("tek")
gl = Gitlab(git_server, private_token=git_token)

table = Table(box=box.MINIMAL)

table.add_column("Project", style="cyan")
table.add_column("MR ID", style="white")
table.add_column("Title", style="white")
table.add_column("Author", style="yellow")
table.add_column("URL", style="blue")

for project in gl.projects.list(all=True):
    try:
        mrs = project.mergerequests.list(state="opened", all=True)
        for mr in mrs:
            table.add_row(
                project.name,
                f"!{mr.iid}",
                mr.title,
                mr.author["name"],
                mr.web_url
            )
    except Exception:
        # certains projets peuvent être inaccessibles selon les droits
        continue

console = Console()
console.print(table)

