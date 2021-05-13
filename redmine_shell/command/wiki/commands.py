''' Wiki Commands. '''


from redmine_shell.shell.command import Command, CommandType
from redmine_shell.shell.switch import get_current_redmine
from redmine_shell.shell.helper import RedmineHelper


class ReadWiki(Command):
    ''' List Wiki Command. '''
    name = "read_wiki"
    DESC = "Read Wiki Page"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        _, url, key = get_current_redmine()
        ri = RedmineHelper(url=url, key=key)
        pid = ri.help_ask_project_number()
        if pid is None:
            return True

        # List-up the wiki pages
        print("--- Available Wiki Pages ---")
        wiki_page_map = {}
        for i, wp in enumerate(ri.wiki_page.filter(project_id=pid), 1):
            print("{}: {}".format(i, wp.title))
            wiki_page_map[i] = wp.title

        wiki = ri.help_ask_wiki_number()
        if wiki is None:
            print("Input is Invalid")
            return True

        if wiki not in wiki_page_map:
            print("Wiki Page Index is Invalid")
            return True

        title = wiki_page_map[wiki]
        try:
            wiki_page = ri.wiki_page.get(title, project_id=pid)
        except:
            print("Cannot load {}'s wiki page".format(title))
            return True
        text = wiki_page.text.replace('\r\n', '\n')
        ri.help_user_input(text.encode())
        return True


class UpdateWiki(Command):
    ''' Update Wiki Command. '''
    name = "update_wiki"
    DESC = "Update Wiki Page"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        _, url, key = get_current_redmine()
        ri = RedmineHelper(url=url, key=key)
        pid = ri.help_ask_project_number()
        if pid is None:
            return True

        # List-up the wiki pages
        print("--- Available Wiki Pages ---")
        wiki_page_map = {}
        for i, wp in enumerate(ri.wiki_page.filter(project_id=pid), 1):
            print("{}: {}".format(i, wp.title))
            wiki_page_map[i] = wp.title

        wiki = ri.help_ask_wiki_number()
        if wiki is None:
            print("Input is Invalid")
            return True

        if wiki not in wiki_page_map:
            print("Wiki Page Index is Invalid")
            return True

        title = wiki_page_map[wiki]
        try:
            wiki_page = ri.wiki_page.get(title, project_id=pid)
        except:
            print("Cannot load {}'s wiki page".format(title))
            return True
        text = wiki_page.text.replace('\r\n', '\n')
        data = ri.help_user_input(text.encode())
        ri.wiki_page.update(title, project_id=pid, text=data)
