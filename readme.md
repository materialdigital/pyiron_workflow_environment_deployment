# Deployment of pyiron workflow environment 
This repository provides the configuration files, needed for the deployment of a pre-configured jupyterhub to run pyiron workflows.

## Content of the repository
| File | Description |
| ----------------- | ----------- |
|`config.json` | a json file containing the needed info for ssl certificate path, keycloak client details, name of pyiron docker images, docker networks, ... |
| `pyiron.env` | includes all the default environmental variable essential for the pyrion service in the compose file |
| `shared.env` | includes all the default environmental variable essential for both pyiron and the postgres database |
| `create_hub.py` | the python script which appends the given key-value pairs in the `config.json` file, as environmental variable into `pyiron.env`, `shared.env`, and `build.env` file.  `build.env` is an additional environment file required for running the compose file. It contains the SSL info, as well as the name of the external nerwork from nginx reverse proxy. |
| `docker-compose.yml` | the compose file, which runs jupyterhub and its Postgres database services. |
   
## Deployment Guide
### The infrastructure, OS and other required packages
As an infrastructure, the deployment requires:  
- A server running a Linux operating system
- Installation of docker engine and docker-compose
- Adequate resources for running jupyterhub: (>2GB of RAM + 2 VCPU) 
- The users' resources on the server should be proportional to the number of users (~2GB of RAM, 2VCPU, 10GB of storage per users)

### Assumptions
- For the authentication of the users, keycloak is assumed as the authentication provider. Therefore, a client id and secret are needed.
- Here, it is assumed that all the jobs are run on the same server as the jupyterhub.
- The configuration of the hostnames is assumed to be done separately by the admin, e.g. creating the A-record, etc

### pyiron docker images  
pyiron offers various docker images corresponding to its modules, atomistics, continuum, md, ... . The docker images are available on docker hub: [https://hub.docker.com/u/pyiron](https://hub.docker.com/u/pyiron), and the corresponding dockerfiles can also be found via [https://github.com/pyiron/docker-stacks](https://github.com/pyiron/docker-stacks).   

### The process of the deployment
1) cloning the current git repository .
2) Providing the values for the keys in the `config.json` file. The keys are:
- `HOST_KEY_PATH`: Path to the SSL key on the server 
- `HOST_CERT_PATH`: Path to the SSL certificate on the server
- `NGINX_NETWORK` : The name of the nginx network (the external network from the reverse proxy)
- `OAUTH2_TOKEN_URL`: Keycloak Tocken URL
- `OAUTH2_AUTHORIZE_URL`:Keycloak authorize URL
- `OAUTH2_USERDATA_URL`: Keycloak userdate URL
- `OAUTH_CALLBACK_URL`: Keycloak call back URL
- `CLIENT_ID`: The client ID defined in Keycloak
- `CLIENT_SECRET`: The secret for the client, provided from the Keycloak instance 
- `PYIRON_BASE`: the relavant information of pyiron_base image in the form of `image_name:tag`
- `PYIRON_ATOMISTIC`:the relavant information of pyiron_atomistics image in the form of `image_name:tag`
- `PYIRON_CONTINUUM`:the relavant information of pyiron_continuum image in the form of `image_name:tag`.
- `PYIRON_EXPERIMENTAL`:the relavant information of pyiron_experimental image in the form of `image_name:tag`
- `MEM_LIMIT`: The limiting amount of RAM per user
- `CPU_LIMIT`: The limiting amount of VCPU per user
- `ADMIN_USER`: The username of jupyterhub admin 
- `POSTGRES_PASSWORD`: A password for the postgres database

3) run the `create_hub.py` script.  
4) run docker-compose script via `docker-compose --env-file build.env up -d`

### A brief view on the files
**`config.json`**
```json
{
    "build": {
        "HOST_KEY_PATH": "path/to/key",
        "HOST_CERT_PATH": "path/to/cert",
        "NGINX_NETWORK": "name of nginx network; external"
    },
    "pyiron": {
        "OAUTH2_TOKEN_URL":"toke_url",
        "OAUTH2_AUTHORIZE_URL":"AUTHORIZE_url",
        "OAUTH2_USERDATA_URL":"USERDATA_url",
        "OAUTH_CALLBACK_URL":"CALLBACK_url",
        "CLIENT_ID":"id",
        "CLIENT_SECRET":"secret",
        "PYIRON_BASE":"base_image:tag",
        "PYIRON_ATOMISTIC":"atomistic_image:tag",
        "PYIRON_CONTINUUM":"continuum_image:tag",
        "PYIRON_EXPERIMENTAL":"experimental_image:tag",
        "MEM_LIMIT":"2G",
        "CPU_LIMIT":"1",
        "ADMIN_USER":"user_name"
    },
    "shared" :{
        "POSTGRES_PASSWORD":"password"
    }
}

```

**`create_hub.py`**
```python3
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

```

**`docker-compose.yml`**
```yaml
version: "3"

services:
  hub-db:
    image: postgres:9.5@sha256:ee604a9025ec864da512736f765ae714112a77ffc39d762c76b67ca0f8597e9e
    container_name: jupyterhub-db
    restart: always
    env_file:
      - shared.env
    volumes:
      - "db:/var/lib/postgresql/data"
    networks:
      - internal

  hub:
    depends_on:
      - hub-db
    image: materialdigital/pyiron-jhub:2021-06-07@sha256:4a3af95fc60d5ad0ac6331721a48271b4f2a4dc3ef2d378c0c06a60a2f3a0831
    restart: always
    container_name: jupyterhub
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:rw"
      - "data:/data"
      - "user_auth_hook.py:user_auth_hook.py:ro"
      - "${HOST_CERT_PATH}:/srv/jupyterhub/secrets/jupyterhub.crt:ro"
      - "${HOST_KEY_PATH}:/srv/jupyterhub/secrets/jupyterhub.key:ro"
    ports:
      - "443:443"
    links:
      - hub-db
    env_file:
      - shared.env
      - pyiron.env
    environment:
      POSTGRES_HOST: hub-db
    command: >
      jupyterhub -f /srv/jupyterhub/jupyterhub_config.py
    networks:
      - internal
      - pmd-server_nginx-net

volumes:
  data:
      name: jupyterhub-data
      driver: local
  db:
      name: jupyterhub-db-data
      driver: local

networks:
  pmd-server_nginx-net:
    external: true
    name: ${NGINX_NETWORK}
  internal:
    name: jupyterhub-network
    driver: bridge

```
### HPC connection (will be added soon)  
In principal, the pyiron docker containers can submit jobs to the cluster according to pyiron documentation in [here](https://pyiron.readthedocs.io/en/latest/source/installation.html#submit-to-remote-hpc).
This feature will be added to pyiron docker images in the next release.

## Room for modification
Here we assumed a semi-automated deployment with minimal changes needed from the side of IT adminstrators. However, many things can be changed, such as:
- building a customized jupyterhub; this gives the possibility to change the jupyterhub configuration
- In the current setup, we assumed to have four jupyter environments based on: `pyiron_base`, `pyiron_atomistics`, and `pyiron_continuum`, `pyiron_experimental`. This list can be extended in the case of a customized jupyterhub build.

