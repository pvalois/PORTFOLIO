#!/usr/bin/env python3

import requests
from lib.credentials import *

(GITLAB_URL, PRIVATE_TOKEN) = get_token("tek")
headers = {
    "PRIVATE-TOKEN": PRIVATE_TOKEN
}

def get_all_projects():
    projects = []
    page = 1
    per_page = 100

    while True:
      url = f"{GITLAB_URL}/api/v4/projects?membership=true&simple=true&per_page={per_page}&page={page}"
      response = requests.get(url, headers=headers)
      response.raise_for_status()
      batch = response.json()

      if not batch: break

      projects.extend(batch)
      page += 1

    return projects

def get_project_variables(project_id):
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/variables"
    response = requests.get(url, headers=headers)
    if response.status_code == 403:
        return []  # Pas les droits, on skippe
    response.raise_for_status()
    return response.json()



if __name__ == "__main__":
  projects = get_all_projects()

  for project in projects:
    pid = project["id"]
    name = project["path_with_namespace"]
    web_url = project["web_url"]
    try:
      issues = []
      for var in get_project_variables(pid):
        key = var["key"]
        if not var.get("masked", False): issues.append(f"🙈 {key} → NON MASQUÉE")
        if not var.get("protected", False): issues.append(f"🔓 {key} → NON PROTÉGÉE")

      print(f"\n🔍 Projet: {name}")
      print(f"🌐 {web_url}")

      if issues:
        for issue in issues: print(issue)
      else: print("✅ Toutes les variables sont sécurisées")

    except requests.exceptions.RequestException as e:
      print(f"❌ Erreur projet {name} ({pid}): {e}")

