# REDMINE SHELL

## Environments

1. Python3.8.5
2. pip
3. python3-venv


## Install

1. Create a virtual environment. `python -m venv ./redmine`
2. Activate the virtual environment. `. ./redmine/bin/activate`
3. Install "redmine_shell". `python ./setup.py install`
4. Create "~/.redmine_shell_rc" file
```json
{
    "your_name": {
        "URL": "http://your.redmine.server.com",
        "KEY": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",  #<-- your redmine key
        "PREVIEW_PROJ_NUM": null,   #optional
        "PREVIEW_WIKI_NAME": null,  #optional
        "PREVIEW_PROJ_NUM": null,   #optional
        "PREVIEW_WIKI_NAME": null,  #optional
        "WEEK_REPORT_ISSUE": null   #optional
    }
}
```
5. Run "redmine_shell". `./start.sh`


## Known Issues

### 1. SSL Verify Issue

* If your redmine server has a self-signed certificate, "redmine_shell" would print many warning messages.
  Because Client side can't verify the server's certificate.
* To surpress the warning messages, you need to edit code in "python-redmine" source code.

```python
#./redmine/lib/python3.8/site-packages/python_redmine-2.3.0-py3.8.egg/redminelib/engines/sync.py

class SyncEngine(BaseEngine):
    @staticmethod
    def create_session(**params):
        session = requests.Session()
        session.verify = False                       #<--- Added
        requests.packages.urllib3.disable_warnings() #<--- Added

        for param in params:
            setattr(session, param, params[param])

        return session
```
