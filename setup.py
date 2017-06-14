#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-keyerror',
    version='3.1.1',
    description='KeyError.com Django client',

    url='https://keyerror.com/docs/django',
    author="Chris Lamb",
    author_email='chris@keyerror.com',

    packages=find_packages(),

    install_requires=(
        'Django>=1.9',
    ),
)
