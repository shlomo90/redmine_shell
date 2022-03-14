# REDMINE SHELL

## Environments

1. Python3.8.5
2. pip
3. python3-venv


## Install

1. Create a virtual environment. `python3 -m venv ./redmine`
2. Activate the virtual environment. `. ./redmine/bin/activate`
3. Install "redmine_shell". `python ./setup.py install`
4. Create "~/.redmine_shell_rc" file
```json
{
    "your_name": {
        "URL": "http://your.redmine.server.com",
        "KEY": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "PREVIEW_PROJ_NUM": null,
        "PREVIEW_WIKI_NAME": null,
        "WEEK_REPORT_ISSUE": null
    }
}


```
* Elements
    * "your_name": Renaming "your_name" for your redmine. This will show on a shell prompt.
    * "URL": Your redmine server URL.
    * "KEY": Your Redmine API Key.
    * "PREVIEW_PROJ_NUM": Experimental.
    * "PREVIEW_PROJ_NAME": Experimental.
    * "PREVIEW_PROJ_NUM": Experimental.
    * "WEEK_REPORT_ISSUE": Experimental.

5. Run "redmine_shell". `./start.sh`

https://user-images.githubusercontent.com/44340022/158195488-f1df194d-77b8-4e8e-be20-34b7cf321bb5.mov


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
