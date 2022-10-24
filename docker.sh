#!/bin/bash

ret=`docker image ls --format "{{.Repository}}" | grep redmine_shell`
if [ "$ret" != "redmine_shell" ]
then
    docker build . -t redmine_shell
fi

ret=`docker container ps -a --format "{{.Names}}" | grep redmine_shell`
if [ "$ret" != "redmine_shell" ]
then
    docker run -d -it --name redmine_shell redmine_shell
fi

ret=`docker container ls --format "{{.Names}}" | grep redmine_shell`
if [ "$ret" != "redmine_shell" ]
then
    docker start redmine_shell
fi

docker exec -it redmine_shell python start.py
