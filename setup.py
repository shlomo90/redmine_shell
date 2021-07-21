import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

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
    install_requires=["python-redmine==2.3.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='==3.8',
)