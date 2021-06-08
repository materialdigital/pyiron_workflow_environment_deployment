#!/usr/bin/python3
import json
import os

cwd = os.getcwd()
static_path = os.path.join(cwd, 'static.json')

if os.path.exists(static_path):
    with open('static.json') as static_file:
        static_data = json.load(static_file)
    for env_file_name in static_data.keys():
        env_file_name_plus_ext = env_file_name+'.env'
        env_path = os.path.join(cwd, env_file_name_plus_ext)
        with open(env_path, "w") as env_file:
            lines = [f'{key}={value}\n' for key, value in static_data[env_file_name].items()]
            print(f"### Writing {env_file_name}")
            env_file.writelines(lines)

with open('config.json') as config_file:
    config_data = json.load(config_file)

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
            lines = [f'{key}={value}\n' for key, value in config_data[env_file_name].items()]
            print(f"### Writing {env_file_name}")
            env_file.writelines(lines)
