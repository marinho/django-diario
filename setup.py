# -*- coding: utf-8 -*-
#
#  Copyright (c) 2007, 2008 Guilherme Mesquita Gondim and contributors
#
#  This file is part of Django Diário.
#
#  Django Diário is free software under terms of the GNU Lesser
#  General Public License version 3 (LGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#


"""
Django Diário setup.
"""

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
from diario import get_version


setup(
    name = 'django-diario',
    version = get_version(),
    description = 'Blog application for Django projects',
    long_description = ('Django Diário is a pluggable weblog application for '
                        'Django Web Framework.'),
    keywords = 'django apps weblog blog',
    author = 'Guilherme Gondim',
    author_email = 'semente@taurinus.org',
    url = 'http://django-diario.googlecode.com',
    download_url = 'http://code.google.com/p/django-diario/downloads/list',
    license = 'GNU Lesser General Public License (LGPL), Version 3',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
)
