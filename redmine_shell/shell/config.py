''' Configuration of Redmine.
'''


DEBUG = False
VERSION = "v0.0.1"
VERSION_CHECK_SERVER = "http://check.server.com"

#  Usage.
#  - vi editor     : vi   (Deafult)
#  - vscode editor : code (Required 'vscode')
DEFAULT_EDITOR = 'vi'

LOGIN = [
        # For My Redmine
        {
            'NAME': "REDMINE",
            'URL': "REDMINE_URL",
            'KEY': "aaaaaaaaaaaaaaaaa",

            # For Preview
            # We need a wiki page in a specific project to show the preview page which
            # current user is editting.
            'PREVIEW_PROJ_NUM': None,
            'PREVIEW_WIKI_NAME': None, },
        {
            'NAME': "EXTRA",
            'URL': "REDMINE_URL...",
            'KEY': "bbbbbbbbbbbbbbbbb",

            # For Preview
            # We need a wiki page in a specific project to show the preview page which
            # current user is editting.
            'PREVIEW_PROJ_NUM': None,
            'PREVIEW_WIKI_NAME': None, },
        ]
