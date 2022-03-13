''' Template Commands. '''


from redmine_shell.shell.command import Command, CommandType
from redmine_shell.shell.inventory import Inventory
from redmine_shell.shell.input import redmine_input



class CreateTemplate(Command):
    ''' Create Template command. '''
    name = "create_tempalte"
    DESC = "Create Template"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, args=None):

        try:
            name = redmine_input("Template Name?: ").strip()
        except EOFError:
            print("")
            return True
        except KeyboardInterrupt:
            print("")
            return True

        if name == '':
            print("Error: Plz Input String!")
            return True
        for template_file in Inventory.get_command_files('template'):
            if name + '.template' == template_file:
                print("Error: name is duplicated.")
                return True

        Inventory.new_command_file(name, 'template')
        return True


class RemoveTemplate(Command):
    ''' Remove Template command. '''

    name = "remove_tempalte"
    DESC = "Remove Template"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, args=None):

        try:
            name = redmine_input("Template Name?: ").strip()
        except EOFError:
            print("")
            return True
        except KeyboardInterrupt:
            print("")
            return True

        if name == '':
            print("Error: Plz Input String!")
            return True

        found = False
        for template_file in Inventory.get_command_files('template'):
            if name + '.template' == template_file:
                found = True
                break

        if found is False:
            print("Error: No name: {} template.".format(name))
            return True

        Inventory.remove_command_file(name, 'template')
        return True


class EditTemplate(Command):
    ''' Edit Template command. '''

    name = "edit_tempalte"
    DESC = "Edit Template"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, args=None):

        try:
            name = redmine_input("Template Name?: ").strip()
        except EOFError:
            print("")
            return True
        except KeyboardInterrupt:
            print("")
            return True

        if name == '':
            print("Error: Plz Input String!")
            return True

        found = False
        for template_file in Inventory.get_command_files('template'):
            if name + '.template' == template_file:
                found = True
                break

        if found is False:
            print("Error: No name: {} template.".format(name))
            return True

        Inventory.edit_command_file(name, 'template')
        return True


class ReadTemplate(Command):
    ''' Read Template command. '''

    name = "read_tempalte"
    DESC = "Read Template"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, args=None):

        try:
            name = redmine_input("Template Name?: ").strip()
        except EOFError:
            print("")
            return True
        except KeyboardInterrupt:
            print("")
            return True

        if name == '':
            print("Error: Plz Input String!")
            return True

        found = False
        for template_file in Inventory.get_command_files('template'):
            if name + '.template' == template_file:
                found = True
                break

        if found is False:
            print("Error: No name: {} template.".format(name))
            return True

        Inventory.read_command_file(name, 'template')
        return True


class ListTemplate(Command):
    ''' List Template command. '''

    name = "list_tempalte"
    DESC = "List Template"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, args=None):
        for template_file in Inventory.get_command_files('template'):
            print(''.join(template_file.split('.')[:-1]))
        return True
