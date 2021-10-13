''' Script Commands. '''


import os
import shutil
import tempfile
from redmine_shell.shell.switch import get_current_redmine
from redmine_shell.shell.command import Command, CommandType
from redmine_shell.shell.input import redmine_input
from redmine_shell.shell.constants import HOME_PATH, DATA_PATH


class ScriptManager():
    ''' Load script files from /opt/redmine_shell.

    Tree:
    opt +
        +- redmine_shell +
                         + <key1> +
                         |        + 1 <-- script file
                         |        + 2
                         + <key2> + 1
                                  + 2
    '''

    def __init__(self, key=None, external_path=None):
        if key is None:
            raise KeyError("Redmine API Key must exists.")

        if external_path is None:
            path = DATA_PATH
        else:
            path = external_path

        self.script = {}
        self.script_key = key
        self.script_key_path = os.path.abspath('/'.join([path, key]))
        self.script_path = os.path.abspath(path)

        self._setup_script_path()
        self._load_script()

    def _setup_script_path(self):
        ''' Setup the script directories Tree. '''

        try:
            os.mkdir(self.script_path)
        except FileExistsError:
            pass

        try:
            os.mkdir(self.script_key_path)
        except FileExistsError:
            pass

    def _load_script(self):
        ''' Load Scripts from the path. '''

        for dpath, dnames, _ in os.walk(self.script_key_path):
            for dname in dnames:
                try:
                    index = int(dname)
                except ValueError:
                    continue

                self.script[index] = {}
                path = '/'.join([dpath, str(index)])
                self.script[index]['path'] = path

                title_path = '/'.join([path, 'title'])
                try:
                    with open(title_path, 'r') as file_obj:
                        title = file_obj.read().strip()
                except FileNotFoundError:
                    title = ''
                self.script[index]['title'] = title

                memo_path = '/'.join([path, 'memo'])
                try:
                    with open(memo_path, 'r') as file_obj:
                        memo = file_obj.read()
                except FileNotFoundError:
                    memo = ''
                self.script[index]['memo'] = memo

            # Only walk one depth.
            break

    def create(self):
        ''' Create Script. '''

        if not self.script:
            idx = 1
        else:
            idx = max(self.script.keys()) + 1

        path = "/".join([self.script_key_path, str(idx)])
        os.mkdir(path)

        title = redmine_input("Title: ").strip()
        os.system("echo {} > {}".format(title, path + '/title'))

        temp = tempfile.NamedTemporaryFile()
        os.system("{} {}".format("vi", temp.name))
        os.system("cp {} {}".format(temp.name, path + '/memo'))
        print("Write done")

    def remove(self, idx):
        ''' Remove Script. '''

        if int(idx) not in self.script:
            print("No Index Input")
            return

        path = "/".join([self.script_key_path, str(idx)])
        shutil.rmtree(path, ignore_errors=True)

        del self.script[int(idx)]
        print("Remove Done")

    def edit(self, idx):
        ''' Edit Script. '''

        if int(idx) not in self.script:
            print("No Index Input")
            return

        key_path = self.script[int(idx)]['path']
        memo_path = '/'.join([key_path, 'memo'])
        os.system('vi {}'.format(memo_path))
        print("edit Done")


class RunScript(Command):
    ''' show_script command. '''
    name = "run_script"
    DESC = "run the script"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, args=None):
        _, _, key = get_current_redmine()
        script = ScriptManager(key=key)

        try:
            idx = redmine_input("Index to run?: ").strip()
        except EOFError:
            print("")
            return True
        except KeyboardInterrupt:
            print("")
            return True

        if idx.isdigit() is False:
            print("Error: Plz Input digital number!")
            return True

        try:
            target = int(idx)
            data = script.script[target]['memo']
        except ValueError:
            print("Error: Input script ID is invalid.")
            return True
        except KeyError:
            print("Error: Input script ID is invalid.")
            return True
        except IndexError:
            print("Error: Input script ID is invalid.")
            return True

        commands = data.strip().split('\n')
        return self.batch(commands)

    def batch(self, commands):
        shell = self.shell
        shell.batch(commands, True)
        return True


class ShowScriptAll(Command):
    ''' show_script_all command. '''
    name = "show_script_all"
    DESC = "Show the all scripts"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        _, _, key = get_current_redmine()
        script = ScriptManager(key=key)
        keys = sorted(script.script.keys())
        print('=================================')
        for k in keys:
            data = script.script[k]
            print("{}: {}".format(k, data['title']))
            print("{}".format(data['memo']))
            if k == keys[-1]:
                break
            print('---------------------------------')
        print('=================================')
        return True


class CreateScript(Command):
    ''' create_script command. '''
    name = "create_script"
    DESC = "Create New Script"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        _, _, key = get_current_redmine()
        script = ScriptManager(key=key)
        script.create()
        return True


class EditScript(Command):
    ''' edit_script command. '''
    name = "edit_script"
    DESC = "Edit the script"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        _, _, key = get_current_redmine()
        script = ScriptManager(key=key)
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

        script.edit(int(idx))
        return True


class RemoveScript(Command):
    ''' remove script command. '''
    name = "remove_script"
    DESC = "Remove the script"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        _, _, key = get_current_redmine()
        script = ScriptManager(key=key)

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

        script.remove(int(idx))
        return True
