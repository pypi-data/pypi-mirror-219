import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.rst show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.rst"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# you need to change all these
VERSION = '0.0.1'
DESCRIPTION = 'easy tool kit'

setup(
    name="generalkit",
    version=VERSION,
    author="wade",
    author_email="wade.xiao.x@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    license='MIT',
    install_requires=[

    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
