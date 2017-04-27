from codecs import open
from os import path

from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()


setup(
    name='cskipdict',
    version='0.0.1',

    description='A fast CFFI-based SkipDict implementation.',
    long_description=readme,
    url='https://github.com/zacharyvoase/python-cskipdict',

    author='Zachary Voase',
    author_email='zack@meat.io',
    license='UNLICENSE',

    packages=find_packages(exclude=['test']),

    setup_requires=["cffi>=1.4.0"],
    cffi_modules=["cskipdict_build.py:ffibuilder"],

    install_requires=["cffi>=1.4.0"],
)
