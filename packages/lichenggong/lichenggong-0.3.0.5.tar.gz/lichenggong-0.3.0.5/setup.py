# coding=utf-8
from setuptools import setup
with open(".\\ver\\Noodows\\version\\version.txt", 'r') as f1:
    version = f1.readline()
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
setup(
    packages=['ver','ver.Noodows','ver.Noodows.version','ver.Program_Files.System','ver.Program_Files.User'],
    name="lichenggong",
    version=version,
    description="python 3   windows 10 (best)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    package_data={'':['*.py','*.txt','*.log']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3")
