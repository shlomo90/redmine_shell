''' Redmine Inventory. '''


from redmine_shell.shell.switch import get_current_redmine_config, get_login
from redmine_shell.shell.constants import DATA_PATH
from os import listdir, system, makedirs
from os.path import isfile, join
import tempfile


class Inventory():
    ''' Redmine Inventory.

    Each redmine 'key' has its own inventory where the directory path is
    "~/.redmine_shell/<key>".

    This class manages files in the directory, creating, deleting, etc.
    Some commands (scripts, template) may create files that are suffixed by
    ".<command>" in the directory to save their objects. '''

    USE_COMMANDS = ['template', 'script']

    @classmethod
    def load_inventory_directories(cls):
        login_instance = get_login()
        for login in login_instance.iterate_login():
            path = cls.get_inventory_path(key=login['KEY'])
            makedirs(path, exist_ok=True)

    @classmethod
    def get_inventory_path(cls, key=None):
        if key is not None:
            return DATA_PATH + '/{}'.format(key)
        else:
            config = get_current_redmine_config()
            return DATA_PATH + '/{}'.format(config['KEY'])

    @classmethod
    def get_command_file_path(cls, name, command):
        path = cls.get_inventory_path()
        return '/'.join([path, name + '.{}'.format(command)])

    @classmethod
    def get_command_files(cls, command):
        if command not in cls.USE_COMMANDS:
            return []

        ret = []
        path = cls.get_inventory_path()
        for file_name in listdir(path):
            abs_file = '/'.join([path, file_name])
            if isfile(abs_file) and file_name.endswith(command):
                ret.append(file_name)
        return ret

    @classmethod
    def new_command_file(cls, name, command):
        if command not in cls.USE_COMMANDS:
            return []

        path = cls.get_inventory_path()
        temp = tempfile.NamedTemporaryFile()
        system('{} {}'.format('vi', temp.name))
        suffix = '.{}'.format(command)
        system('cp {} {}'.format(temp.name, '/'.join([path, name + suffix])))
        print("Write done")

    @classmethod
    def remove_command_file(cls, name, command):
        if command not in cls.USE_COMMANDS:
            return []

        config = get_current_redmine_config()
        path = '/'.join([DATA_PATH, config['KEY'], name + '.{}'.format(command)])
        system('rm -f {}'.format(path))

    @classmethod
    def edit_command_file(cls, name, command):
        if command not in cls.USE_COMMANDS:
            return []

        path = cls.get_command_file_path(name, command)
        system('vi {}'.format(path))

    @classmethod
    def read_command_file(cls, name, command):
        if command not in cls.USE_COMMANDS:
            return []

        path = cls.get_command_file_path(name, command)
        with open(path, 'r') as f:
            print(f.read())
