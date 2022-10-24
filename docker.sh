#!/bin/bash

ret=`docker image ls --format "{{.Repository}}" | grep redmine_shell`
if [ "$ret" != "redmine_shell" ]
then
    docker build . -t redmine_shell
fi

ret=`docker container ps -a --format "{{.Names}}" | grep redmine_shell`
if [ "$ret" == "redmine_shell" ]
then
    docker start -a -i redmine_shell
else
    docker run -it --name redmine_shell redmine_shell
fi
