#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import os.path
import warnings
import sys

try:
    from setuptools import setup, Command
    setuptools_available = True
except ImportError:
    setuptools_available = False

# Package Info
# ----------------------------------------------------

PKG = 'mediarenamer'

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.rst') as changelog_file:
    history = changelog_file.read()

# Get the version from mediarenamer/version.py without importing the package
exec(compile(open('mediarenamer/version.py').read(),
             'mediarenamer/version.py', 'exec'))

classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.13',
    'Natural Language :: English',
    'Topic :: Multimedia',
    'Topic :: Multimedia :: Video',
    'Topic :: Desktop Environment :: File Managers',
    'Topic :: Utilities',
    'Operating System :: Microsoft',
    'Operating System :: Microsoft :: Windows',
    ]

requirements = [
    'argparse',
]

test_requirements = []

# Package Setup
# ----------------------------------------------------

setup(
    name=PKG,
    version=__version__,
    description='Media handling and processing for Plex library',
    long_description=readme + '\n\n' + history,
    author='Andrew Hale',
    author_email='halea2196@gmail.com',
    url='https://github.com/alhale2196/MediaRenamer',
    packages=['mediarenamer'],
    package_dir={'mediarenamer': 'mediarenamer'},
    entry_points={
        'console_scripts': [
            'mediarenamer=mediarenamer.mediarenamer:main',
        ]
    },
    install_requires=requirements,
    license='MIT license',
    zip_safe=False,
    keywords='',
    classifiers=classifiers,
    test_suite='tests',
    tests_require=test_requirements,
    )
