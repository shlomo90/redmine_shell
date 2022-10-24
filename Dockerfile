FROM python:3

WORKDIR /usr/src/app

#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt

# Install MariaDB(It's necessary to install mariadb by pip.)
RUN apt update -y
RUN wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
RUN echo "733cf126b03f73050e242102592658913d10829a5bf056ab77e7f864b3f8de1f  mariadb_repo_setup" | sha256sum -c -
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup --mariadb-server-version="mariadb-10.6"
RUN apt install libmariadb3 libmariadb-dev -y
RUN pip install mariadb

# Install Editor.
RUN apt install vim -y

# Install Redmine Shell
COPY ./redmine_shell ./redmine_shell
COPY ./start.py ./start.py
COPY ./setup.py ./setup.py
COPY ./README.md ./README.md
COPY ./.redmine_shell_rc /root/.redmine_shell_rc

RUN python setup.py install

#CMD [ "python", "./your-daemon-or-script.py" ]
ENTRYPOINT [ "python", "start.py" ]
