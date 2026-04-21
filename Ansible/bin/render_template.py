#!/usr/bin/env python3

import argparse
import os
import sys
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateError
from colorama import init, Fore, Style

init(autoreset=True)

def load_yaml_file(filepath):
    if not os.path.isfile(filepath):
        print(Fore.CYAN + f"Warning: YAML file {filepath} not found, skipping.")
        return {}
    try:
        with open(filepath, 'r') as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        print(Fore.RED + f"Error parsing YAML file {filepath}: {e}")
        sys.exit(1)

def merge_dicts(d1, d2):
    # simple deep merge for dicts, d2 overrides d1
    for k, v in d2.items():
        if isinstance(v, dict) and k in d1 and isinstance(d1[k], dict):
            merge_dicts(d1[k], v)
        else:
            d1[k] = v

def parse_var_string(var_string):
    if '=' not in var_string:
        print(Fore.RED + f"Invalid --var format (expected key=value): {var_string}")
        sys.exit(1)
    key, val = var_string.split('=', 1)
    return key.strip(), val.strip()

def main():
    parser = argparse.ArgumentParser(description="Render a Jinja2 template with Ansible-like vars loading")
    parser.add_argument('-t', '--template', required=True, help="Path to Jinja2 template file")
    parser.add_argument('--load', help="Comma separated list of additional YAML files to load after defaults/vars")
    parser.add_argument('--var', action='append', help="Override/add variables (key=value), can be used multiple times")

    args = parser.parse_args()

    template_path = os.path.abspath(args.template)
    if not os.path.isfile(template_path):
        print(Fore.RED + f"Template file {template_path} not found")
        sys.exit(1)

    template_dir = os.path.dirname(template_path) or "."

    vars_data = {}

    # Load defaults/main.yml from template_dir or cwd
    defaults_path = os.path.join(template_dir, "defaults", "main.yml")
    if not os.path.isfile(defaults_path):
        defaults_path = os.path.join(os.getcwd(), "defaults", "main.yml")
    merge_dicts(vars_data, load_yaml_file(defaults_path))

    # Load vars/main.yml from template_dir or cwd
    vars_path = os.path.join(template_dir, "vars", "main.yml")
    if not os.path.isfile(vars_path):
        vars_path = os.path.join(os.getcwd(), "vars", "main.yml")
    merge_dicts(vars_data, load_yaml_file(vars_path))

    # Load extra yaml files from --load option (comma separated)
    if args.load:
        for yaml_file in args.load.split(','):
            yaml_file = yaml_file.strip()
            if not yaml_file:
                continue
            yaml_path = os.path.abspath(yaml_file)
            if not os.path.isfile(yaml_path):
                print(Fore.CYAN + f"Warning: Additional YAML file {yaml_path} not found, skipping.")
                continue
            merge_dicts(vars_data, load_yaml_file(yaml_path))

    # Override/add variables from --var
    if args.var:
        for var_str in args.var:
            key, val = parse_var_string(var_str)
            vars_data[key] = val

    # Setup Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(template_dir),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )

    try:
        template_rel_path = os.path.relpath(template_path, template_dir)
        template = env.get_template(template_rel_path)
        rendered = template.render(vars_data)
    except TemplateError as e:
        print(Fore.RED + f"Error rendering template: {e}")
        sys.exit(1)

    print(rendered)


if __name__ == "__main__":
    main()
