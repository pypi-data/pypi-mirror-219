#!/usr/bin/python3

import codecs
import os
import re

from setuptools import setup, find_packages

long_description = """Copr is designed to be a lightweight buildsystem that allows contributors
to create packages, put them in repositories, and make it easy for users
to install the packages onto their system. Within the Fedora Project it
is used to allow packagers to create third party repositories.

This part is a command line interface to use copr."""

__description__ = "CLI tool to run copr"
__author__ = "Pierre-Yves Chibon"
__author_email__ = "pingou@pingoured.fr"
__url__ = "https://github.com/fedora-copr/copr"


setup(
    name='mockbuild',
    version="0.0",
    description="Locked for https://github.com/rpm-software-management/mock",
    long_description="Locked for https://github.com/rpm-software-management/mock",
    author="RPM Software Management Team",
    url=__url__,
    license='GPLv2+',
)
