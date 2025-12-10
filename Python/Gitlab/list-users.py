#!/usr/bin/env python3 


from gitlab import *
from dumper import dump
import json
import sys
from pprint import pprint
from lib.credentials import *
from rich.console import Console
from rich.table import Table
from rich.text import Text

(git_server,git_token)=get_token("server")
gl = Gitlab(git_server,oauth_token=git_token)

console=Console()
table = Table(show_header=True, header_style="bold cyan", border_style="bright_black")
table.add_column("Nom", width=25)
table.add_column("Id", width=10)
table.add_column("Login", width=15)
table.add_column("email", width=25)

obj=[]

for user in gl.users.list():
  table.add_row(user.name,str(user.id),user.username,user.email)

console.print (table)



