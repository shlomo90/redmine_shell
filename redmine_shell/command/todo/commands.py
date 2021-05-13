''' Todo Commands. '''


import os
import shutil
import tempfile
from redmine_shell.shell.switch import get_current_redmine
from redmine_shell.shell.command import Command, CommandType
from redmine_shell.shell.input import redmine_input


HOME_PATH = os.getenv('HOME')
BOOKMARK_PATH = HOME_PATH + '/.redmine_shell'


class TodoManager():
    ''' Load todo files from /opt/redmine_shell.

    Tree:
    opt +
        +- redmine_shell +
                         + <key1> +
                         |        + 1 <-- todo file
                         |        + 2
                         + <key2> + 1
                                  + 2
    '''

    def __init__(self, key=None, external_path=None):
        if key is None:
            raise KeyError("Redmine API Key must exists.")

        if external_path is None:
            path = BOOKMARK_PATH
        else:
            path = external_path

        self.todo = {}
        self.todo_key = key
        self.todo_key_path = os.path.abspath('/'.join([path, key]))
        self.todo_path = os.path.abspath(path)

        self._setup_todo_path()
        self._load_todo()

    def _setup_todo_path(self):
        ''' Setup the todo directories Tree. '''

        try:
            os.mkdir(self.todo_path)
        except FileExistsError:
            pass

        try:
            os.mkdir(self.todo_key_path)
        except FileExistsError:
            pass

    def _load_todo(self):
        ''' Load Todos from the path. '''

        for dpath, dnames, _ in os.walk(self.todo_key_path):
            for dname in dnames:
                try:
                    index = int(dname)
                except ValueError:
                    continue

                self.todo[index] = {}
                path = '/'.join([dpath, str(index)])
                self.todo[index]['path'] = path

                title_path = '/'.join([path, 'title'])
                try:
                    with open(title_path, 'r') as file_obj:
                        title = file_obj.read().strip()
                except FileNotFoundError:
                    title = ''
                self.todo[index]['title'] = title

                memo_path = '/'.join([path, 'memo'])
                try:
                    with open(memo_path, 'r') as file_obj:
                        memo = file_obj.read()
                except FileNotFoundError:
                    memo = ''
                self.todo[index]['memo'] = memo

            # Only walk one depth.
            break

    def create(self):
        ''' Create Todo. '''

        if not self.todo:
            idx = 1
        else:
            idx = max(self.todo.keys()) + 1

        path = "/".join([self.todo_key_path, str(idx)])
        os.mkdir(path)

        title = redmine_input("Title: ").strip()
        os.system("echo {} > {}".format(title, path + '/title'))

        temp = tempfile.NamedTemporaryFile()
        os.system("{} {}".format("vi", temp.name))
        os.system("cp {} {}".format(temp.name, path + '/memo'))
        print("Write done")

    def remove(self, idx):
        ''' Remove Todo. '''

        if int(idx) not in self.todo:
            print("No Index Input")
            return

        path = "/".join([self.todo_key_path, str(idx)])
        shutil.rmtree(path, ignore_errors=True)

        del self.todo[int(idx)]
        print("Remove Done")

    def edit(self, idx):
        ''' Edit Todo. '''

        if int(idx) not in self.todo:
            print("No Index Input")
            return

        key_path = self.todo[int(idx)]['path']
        memo_path = '/'.join([key_path, 'memo'])
        os.system('vi {}'.format(memo_path))
        print("edit Done")


class ShowTodo(Command):
    ''' show_todo command. '''
    name = "show_todo"
    DESC = "show current todo"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        _, _, key = get_current_redmine()
        todo = TodoManager(key=key)
        keys = sorted(todo.todo.keys())
        print('=================================')
        for k in keys:
            data = todo.todo[k]
            print("{}: {}".format(k, data['title']))
            #print("{}".format(data['memo']))
            if k == keys[-1]:
                break
            print('---------------------------------')
        print('=================================')
        return True


class ShowTodoAll(Command):
    ''' show_todo_all command. '''
    name = "show_todo_all"
    DESC = "Show the all todos"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        _, _, key = get_current_redmine()
        todo = TodoManager(key=key)
        keys = sorted(todo.todo.keys())
        print('=================================')
        for k in keys:
            data = todo.todo[k]
            print("{}: {}".format(k, data['title']))
            print("{}".format(data['memo']))
            if k == keys[-1]:
                break
            print('---------------------------------')
        print('=================================')
        return True


class CreateTodo(Command):
    ''' create_todo command. '''
    name = "create_todo"
    DESC = "Create New Todo"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        _, _, key = get_current_redmine()
        todo = TodoManager(key=key)
        todo.create()
        return True


class EditTodo(Command):
    ''' edit_todo command. '''
    name = "edit_todo"
    DESC = "Edit the todo"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        _, _, key = get_current_redmine()
        todo = TodoManager(key=key)
        try:
            idx = redmine_input("Index to edit?: ").strip()
        except EOFError:
            print("")
            return True
        except KeyboardInterrupt:
            print("")
            return True

        if idx.isdigit() is False:
            print("Error: Plz Input digital number!")
            return True

        todo.edit(int(idx))
        return True


class RemoveTodo(Command):
    ''' remove todo command. '''
    name = "remove_todo"
    DESC = "Remove the todo"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        _, _, key = get_current_redmine()
        todo = TodoManager(key=key)

        try:
            idx = redmine_input("Index to remove?: ").strip()
        except EOFError:
            print("")
            return True
        except KeyboardInterrupt:
            print("")
            return True

        if idx.isdigit() is False:
            print("Error: Plz Input digital number!")
            return True

        todo.remove(int(idx))
        return True
