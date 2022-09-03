from __future__ import print_function
from setuptools import setup
import sys
import os

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), 'jhsiao'))
from namespace import make_ns

make_ns('jhsiao')
setup(
    name='jhsiao.namespace',
    version='0.0.1',
    author='Jason Hsiao',
    author_email='oaishnosaj@gmail.com',
    description='manage add pkgutil namespace __init__.py',
    py_modules=['jhsiao.namespace']
)
