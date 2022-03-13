''' Redmine Inventory. '''


from redmine_shell.shell.switch import get_current_redmine_config
from redmine_shell.shell.constants import DATA_PATH
from os import listdir, system
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
    def get_command_files(cls, command):

        if command not in cls.USE_COMMANDS:
            return []

        config = get_current_redmine_config()
        path = DATA_PATH + '/{}'.format(config['KEY'])

        ret = []
        for file_name in listdir(path):
            abs_file = '/'.join([path, file_name])
            if isfile(abs_file) and file_name.endswith(command):
                ret.append(file_name)
        return ret

    @classmethod
    def new_command_file(cls, name, command):
        if command not in cls.USE_COMMANDS:
            return []

        config = get_current_redmine_config()
        path = '/'.join([DATA_PATH, config['KEY']])

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

        config = get_current_redmine_config()
        path = '/'.join([DATA_PATH, config['KEY'], name + '.{}'.format(command)])
        system('vi {}'.format(path))

    @classmethod
    def read_command_file(cls, name, command):
        if command not in cls.USE_COMMANDS:
            return []

        config = get_current_redmine_config()
        path = '/'.join([DATA_PATH, config['KEY'], name + '.{}'.format(command)])
        with open(path, 'r') as f:
            print(f.read())
