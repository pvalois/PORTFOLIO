#!/usr/bin/env python3

from gitlab import *
from gitlab.exceptions import *
from lib.credentials import get_token
from datetime import datetime, timedelta, timezone 
import argparse

# Récupération et établissement de la connexion
(git_server, git_token) = get_token("server")
gl = Gitlab(git_server, oauth_token=git_token)

#Global vars
TARGET_PROJECT_PATH = None
AGE_THRESHOLD_DAYS = 30
DRY_RUN = True

parser = argparse.ArgumentParser( description="Liste et nettoie les artefacts des Jobs GitLab anciens.")
parser.add_argument( 'project_path', type=str, help="Chemin complet du projet GitLab (ex: mon-groupe/mon-projet).")
args = parser.parse_args()

project = gl.projects.get(args.project_path)

jobs = project.jobs.list(all=True, status='finished') 
for job in jobs:
    print(job.id, job.name, job.status)
    endpoint = f'/projects/{project.id}/jobs/{job.id}/artifacts'
    gl.http_delete(endpoint)
    print(f"  ---> ✅ Artefacts du Job {job.id} SUPPRIMÉS.")

