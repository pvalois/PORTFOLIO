#!/usr/bin/env python3


from gitlab import *
from dumper import dump
import json
import sys
from lib.credentials import *

(git_server,git_token)=get_token("server")
gl = Gitlab(git_server,oauth_token=git_token)

print(">> queue metrics")
print(json.dumps(gl.sidekiq.queue_metrics(),indent=2))
print ("")

print(">> process metrics")
print(json.dumps(gl.sidekiq.process_metrics(),indent=2))
print ("")

print(">> job stats")
print(json.dumps(gl.sidekiq.job_stats(),indent=2))
print ("")

print(">> compound metrics")
print(json.dumps(gl.sidekiq.compound_metrics(),indent=2))
print ("")


