#!/usr/bin/env python3
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='zadanko',
    version='1.0.0',
    description="math worksheet generator",
    long_description=readme,
    long_description_content_type='text/markdown',
    author='jacadzaca',
    author_email='vitouejj@gmail.com',
    url='https://github.com/jacadzaca/zadanko',
    license='GPL3',
    packages=find_packages(exclude=('tests', 'docs', 'venv'))
)
