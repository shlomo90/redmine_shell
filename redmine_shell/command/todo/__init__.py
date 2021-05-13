''' Redmine Todo Command. '''


from redmine_shell.shell.config import DEBUG
from redmine_shell.shell.command import Command, CommandType
from redmine_shell.command.todo.commands import (
    ShowTodo, CreateTodo, EditTodo, RemoveTodo, ShowTodoAll)


COMMAND = [
        ShowTodo("show_todo"),
        ShowTodoAll("show_todo_all"),
        CreateTodo("create_todo"),
        EditTodo("edit_todo"),
        RemoveTodo("remove_todo"),
]


class RedmineTodo(Command):
    ''' Redmine Todo Class. '''

    CHILDREN = COMMAND
    DESC = "Todo setting for Redmine."

    def _init_type(self):
        self.type = CommandType.CONTAINER

    def run(self):
        """ EXECUTE TYPE COMMAND SHOULD BE OVERRIDEN """
        raise NotImplementedError("name:{} function:run".format(self.name))
