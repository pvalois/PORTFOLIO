#!/usr/bin/env python3 

import os
from pathlib import Path

import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def lint_file(path):
    result = subprocess.run(["ansible-lint", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if result.returncode != 0:
        return path

    return None

fichiers = []
non_conformes = []

if (os.path.exists("non_conformes.list")):
    with open("non_conformes.list", "r") as f:
        dossiers = [ligne.strip() for ligne in f.readlines() if ligne.strip()]
else:
    roles_dir = Path("/home/valois/ansible/roles/")
    dossiers = sorted([d for d in roles_dir.iterdir() if d.is_dir()])

for dossier in dossiers:
    if (os.path.exists(dossier)):
        fichiers.append(dossier)

with ThreadPoolExecutor(max_workers=8) as executor:
  futures = {executor.submit(lint_file, f): f for f in fichiers}
  for future in as_completed(futures):
    resultat = future.result()
    if resultat:
      if (not resultat in non_conformes): 
        print(resultat)
        non_conformes.append(resultat)

with open("non_conformes.list","w") as f:
  for name in sorted(non_conformes):
    f.write(str(name)+"\n")

