#!/usr/bin/env python3

from aws_local import client
from pprint import pprint

iam = client("iam")

response = iam.list_roles()
roles = response.get("Roles", [])

response = iam.list_users()
users = response.get("Users", [])

print(f"Total Users IAM: {len(users)}")

for user in users:
    user_name = user['UserName']
    user_detail = iam.get_user(UserName=user_name)
    pprint(user_detail['User'])

print ()

print(f"Total roles IAM: {len(roles)}")

for role in roles:
    role_name = role['RoleName']
    role_detail = iam.get_role(RoleName=role_name)
    pprint(role_detail['Role'])

