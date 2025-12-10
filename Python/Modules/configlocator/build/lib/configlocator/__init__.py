#!/usr/bin/env python3

import os
import configparser

def configlocator(filename):
    paths_to_check = [
        os.path.join(os.getcwd(), filename),
        os.path.join(os.path.expanduser("~/"), "."+filename),
        os.path.join("/etc", filename)
    ]

    for path in paths_to_check:
        if os.path.isfile(path):
            config = configparser.ConfigParser()
            config.read(path)
            return config

    raise FileNotFoundError(f"Pas de fichier de config '{filename}'")
