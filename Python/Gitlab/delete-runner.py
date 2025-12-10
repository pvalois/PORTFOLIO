#!/usr/bin/env python3 

import gitlab
from lib.credentials import *
import argparse

(git_server,git_token)=get_token("server")

parser = argparse.ArgumentParser(description="Delete Gitlab Runner")
parser.add_argument('-i', '--runnerid', type=str, required=True, help='Identifiant du runner')
args = parser.parse_args()

gl = gitlab.Gitlab(git_server, private_token=git_token)

try:
  runner = gl.runners.get(args.runnerid)
  runner.delete()
  print(f"Runner {args.runnerid} supprimé avec succès.")
except Exception as e:
  print (e)

