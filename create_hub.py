import json
import os

f = open('auto_config.json',)
data = json.load(f)
with open(".env","a+") as env_file:
    for key1 in list(data.keys()):
            for key2 in list(data[key1].keys()):
                env_file.write(key2+"="+data[key1][key2]+"\n")

os.system("docker network create jupyterhub-network")
os.system("docker volume create jupyterhub-data")
os.system("docker volume create jupyterhub-db-data")
os.system("docker-compose up -d")
