''' Configure Commands. '''


from redmine_shell.shell.config import DEBUG
from redmine_shell.shell.command import Command, CommandType
from redmine_shell.command.configure.commands import (
    CreateUser, DeleteUser
)


COMMAND = [CreateUser('create_user'), DeleteUser('delete_user')]


class RedmineConfigure(Command):
    CHILDREN = COMMAND
    DESC = "Edit Redmine Configure"

    def __init__(self, name):
        super(RedmineConfigure, self).__init__(name)


    def _init_type(self):
        self.type = CommandType.CONTAINER
