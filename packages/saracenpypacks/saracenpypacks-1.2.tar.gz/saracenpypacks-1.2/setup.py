from setuptools import setup, find_packages
import codecs
import json
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

with open("packages.json", "r") as f:
    packages = json.load(f)

VERSION = '1.2'
DESCRIPTION = ''
LONG_DESCRIPTION = ''

# Setting up
setup(
    name="saracenpypacks",
    version=VERSION,
    author="Saracen Rhue",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=packages,
    keywords=['python', 'db'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)