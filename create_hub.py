#!/usr/bin/python3
import json
import os

f = open('config.json',)
config_data = json.load(f)

for env_file_name in config_data.keys():
    env_file_name_plus_ext = env_file_name+'.env'
    cwd = os.getcwd()
    env_path = os.path.join(cwd, env_file_name_plus_ext)
    if os.path.exists(env_path):
        with open(env_path, "a+") as env_file:
            lines = [f'{key}={value}\n' for key, value in config_data[env_file_name].items()]
            print(f"### Writing {env_file_name}")
            env_file.writelines(lines)
    else:
        with open(env_path, "w") as env_file:
            lines = [f'{key}={value}' for key, value in config_data[env_file_name].items()]
            print(f"### Writing {env_file_name}")
            env_file.writelines(lines)
