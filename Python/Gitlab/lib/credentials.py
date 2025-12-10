#!/usr/bin/env python3

import configlocator

def get_token(profile):
  config=configlocator.configlocator("gitlab.ini")
  cred=config[profile]

  #for key in cred: print (key,"->",cred[key])

  return((cred["url"],cred["token"]))
