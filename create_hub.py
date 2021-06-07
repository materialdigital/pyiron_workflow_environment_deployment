#!/usr/bin/python3
import json
import os

f = open('auto_config.json',)
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
try:
    if 'PYIRON_BASE' in config_data['pyiron']:
        image = config_data['pyiron']['PYIRON_BASE']
        os.system(f'docker pull {image}')

    if 'PYIRON_ATOMISTIC' in config_data['pyiron']:
        image = config_data['pyiron']['PYIRON_ATOMISTIC']
        os.system(f'docker pull {image}')
    
    if 'PYIRON_CONTINUUM' in config_data['pyiron']:
        image = config_data['pyiron']['PYIRON_CONTINUUM']
        os.system(f'docker pull {image}')

    if 'PYIRON_EXPERIMENTAL' in config_data['pyiron']:
        image = config_data['pyiron']['PYIRON_EXPERIMENTAL']
        os.system(f'docker pull {image}')
    
except Exception as err_msg:
    print(f"pulling the docker images failed: {err_msg}")
