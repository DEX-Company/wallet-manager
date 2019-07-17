#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup
import os
from os.path import join

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()

install_requirements = [
    'starfish-py==0.4.11',
]

setup_requirements = ['pytest-runner', ]

test_requirements = [
    'codacy-coverage',
    'coverage',
    'docker',
    'flake8',
    'mccabe',
    'pyflakes',
    'pytest',
    'tox',
]

dev_requirements = [
    'bumpversion',
    'pkginfo',
    'twine',
    'watchdog',
]


packages = []
for d, _, _ in os.walk('wallet_manager'):
    if os.path.exists(join(d, '__init__.py')):
        packages.append(d.replace(os.path.sep, '.'))

setup(
    author="dex-company",
    author_email='devops@dex.sg',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="Wallet Manager for the Ocean Network",
    extras_require={
        'test': test_requirements,
        'dev': dev_requirements + test_requirements,
    },
    install_requires=install_requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='wallet manager',
    name='walet-manager',
    packages=packages,
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/DEX-Company/wallet-manager',
    version='0.0.1',
    zip_safe=True,
)
