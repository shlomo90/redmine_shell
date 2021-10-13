""" Redmine Command Class. """


from enum import Enum
from redmine_shell.shell.error import InputError


class CommandType(Enum):
    """ Redmine Command Types. """
    CONTAINER = 0
    EXECUTE = 1
    SYSTEM = 2


class Command():
    """ Basic Command Class.

    This class has basic functions of relationship between parent and children.
    The "run" function is for EXECUTE command type not CONTAINER.
    To make commands as hiarachy Each class that inherits "Command" should
    redefine the "CHILDREN" variable. Each child automatically sets its
    parent when "load_children()" is called.
    Remember that only "CONTAINER" command has a child.

    CONTAINER TYPE COMMAND SHOULD BE OVERRIDEN
    ex: CHILDREN = [CommandClass("command_name"), ]
    """

    CHILDREN = []
    DESC = "No Description"

    #Redmine Connector
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []
        self._init_type()

    def _init_type(self):
        if self.CHILDREN:
            self.type = CommandType.CONTAINER
        else:
            self.type = CommandType.EXECUTE

    def connect_shell(self, shell):
        self.shell = shell
        self._connect_cascade(shell)

    def _connect_cascade(self, shell):
        """ Load Children. """
        children = self.CHILDREN
        for child in children:
            child.connect_shell(shell)

    def add_child(self, command):
        """ Set a command as a child. """

        if command in self.children:
            return

        self.children.append(command)
        command.add_parent(self)

    def add_parent(self, command):
        """ Set a command as a parent. """

        if self.parent is None:
            self.parent = command
        elif self.parent == command:
            return
        else:
            raise InputError("Already There is a parent")

    def get_children(self):
        """ Return children list. """
        return self.children

    def load_children(self):
        """ Load Children. """
        children = self.CHILDREN
        for child in children:
            self.add_child(child)
            child.load_children()

    def run(self):
        """ EXECUTE TYPE COMMAND SHOULD BE OVERRIDEN """
        raise NotImplementedError("name:{} function:run".format(self.name))
