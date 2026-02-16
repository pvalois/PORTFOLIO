#!/usr/bin/env python3

from grafana_api.grafana_face import GrafanaFace
from configlocator import configlocator
from rich.console import Console
from rich.table import Table, box

config = configlocator("grafana.ini")
cred = config['dockerized']

hostname = cred["hostname"]
port = cred["port"]
apikey = cred["apikey"]

base_url = f"http://{hostname}:{port}"

grafana_api = GrafanaFace(
    auth=apikey,
    host=f"{hostname}:{port}"
)

dashboards = grafana_api.search.search_dashboards()

console = Console()
table = Table(box=box.SIMPLE_HEAVY)

table.add_column("Nom du Dashboard", style="cyan", no_wrap=True)
table.add_column("URL complète", style="green")

for dash in dashboards:
    name = dash.get("title", "N/A")
    relative_url = dash.get("url", "")
    full_url = f"{base_url}{relative_url}"
    table.add_row(name, full_url)

console.print(table)

