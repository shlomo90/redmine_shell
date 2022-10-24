# Redmine Shell

This repository is Redmine command line shell program. It works based on a docker container.
We provide a Dockerfile to build the redmine shell image and highly recommend run this program on the docker container.


## Requirements

1. Docker


## Run redmine_shell as Docker Container

1. Execute "sudo ./docker.sh"

## Run redmine_shell with host python

1. Create a virtual environment. `python3 -m venv ./redmine`
2. Activate the virtual environment. `. ./redmine/bin/activate`
3. Install "redmine_shell". `python ./setup.py install`
4. Execute `python ./start.py`
