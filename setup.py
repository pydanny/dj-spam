#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = "0.2.0"

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='dj-spam',
    version=version,
    description="""Django + Fighting Spam Made Easy""",
    long_description=readme + '\n\n' + history,
    author='Daniel Roy Greenfeld',
    author_email='pydanny@gmail.com',
    url='https://github.com/pydanny/dj-spam',
    packages=[
        'spam',
    ],
    include_package_data=True,
    install_requires=[
        'django>=1.8.0',
        'wheel>=0.24.0'
    ],
    license="BSD",
    zip_safe=False,
    keywords='dj-spam',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=[
        "django>=1.8.0",
        "coverage",
        "coveralls",
        "mock>=1.0.1",
        "flake8>=2.1.0",
        "tox>=1.7.0",
        "django-test-plus>=1.0.7"
    ]
)
