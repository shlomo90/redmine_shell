import setuptools
import os
import sys
import json

with open("README.md", "r") as fh:
    long_description = fh.read()

ret = os.system("pip3 install pyperclip3")
print(ret)
if ret:
    pass
else:
    setuptools.setup(
        name="redmine-shell-pkg",
        version="0.0.1",
        author="yourname",
        author_email="example@mail.com",
        description="Simple shell for redmine",
        long_description=long_description,
        long_description_content_type="text/markdown",
        #find_packages finds automatically packages we use
        packages=setuptools.find_packages(),
        install_requires=["python-redmine==2.3.0",
                          "pyperclip3"],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='==3.8',
    )

rs_rc_path = '/'.join([os.environ.get("HOME"), '.redmine_shell_rc'])
if os.path.isfile(rs_rc_path) is True:
    sys.exit(0)
with open(rs_rc_path, 'w') as f:
    config = {}
    config['YOUR_NAME'] = {}
    config['YOUR_NAME']['URL'] = 'http://your.redmine.server.com'
    config['YOUR_NAME']['KEY'] = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    config['YOUR_NAME']['USE_TEMPLATE'] = True
    json.dump(config, f, indent=4)

print("######################### NOTICE #######################")
print("#                                                      #")
print("# Please complete your ~/.redmine_shell_rc file.       #")
print("#                                                      #")
print("########################################################")
