#!/usr/bin/env python3
import argparse
import time
import re
from datetime import datetime
from gitlab import Gitlab
from lib.credentials import *
from textwrap import wrap

# --- CLI ---
parser = argparse.ArgumentParser(description="Afficher les logs d'un pipeline GitLab")
parser.add_argument("-p", "--project", required=True, help="Projet (namespace/project)")
parser.add_argument("-i", "--pipeline-id", type=int, required=True, help="ID du pipeline")
parser.add_argument("-f", "--follow", action="store_true", help="Suivre les logs (mode live-ish)")
parser.add_argument("-t", "--interval", type=int, default=3, help="Intervalle de polling en secondes (défaut: 3)")
args = parser.parse_args()

# --- GitLab ---
(git_server, git_token) = get_token("tek")
gl = Gitlab(git_server, private_token=git_token)
gl.auth()

# --- Projet ---
try:
    project = gl.projects.get(args.project)
except:
    print(f"Can't load project '{args.project}'")
    exit(1)

# --- Pipeline ---
try:
    pipeline = project.pipelines.get(args.pipeline_id)
except:
    print(f"Can't load pipeline {args.pipeline_id}")
    exit(1)

# --- Utils ---
def parse_line(line):
    m = re.match(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z)\s+(\S+)\s*(.*)$", line)
    if m:
        iso_ts, code, msg = m.groups()
        try:
            dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
            human_ts = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            human_ts = iso_ts
        return human_ts, code, msg
    else:
        return "", "", line

def print_line(number, ts, code, msg):
    print(f"{number:4} {ts:19} {msg}")

def follow_job(job, interval):
    last_len = 0
    while True:
        text = job.trace().decode("utf-8", errors="replace")  # <--- correct
        lines = text.splitlines()
        new_lines = lines[last_len:]
        for idx, line in enumerate(new_lines, start=last_len+1):
            ts, code, msg = parse_line(line)
            print_line(idx, ts, code, msg)
        last_len = len(lines)
        job.refresh()
        if job.status in ("success", "failed", "canceled"):
            break
        time.sleep(interval)

# --- Logs ---
jobs_partial = pipeline.jobs.list(all=True)

for job_partial in jobs_partial:

    job = project.jobs.get(job_partial.id)
    print(f"===== {job.name} (id={job.id}, status={job.status}) =====\n")

    if args.follow:
        follow_job(job, args.interval)
        print(f"[END] {job.name} → {job.status}\n")
    else:
        text = job.trace().decode("utf-8", errors="replace")  # <--- correct
        for idx, line in enumerate(text.splitlines(), start=1):
            ts, code, msg = parse_line(line)
            print_line(idx, ts, code, msg)

    print ("\n")
