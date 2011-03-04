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
Blog application for Django projects.
"""

VERSION = (0, 3, 'pre')

def get_version():
    """
    Returns the version as a human-format string.
    """
    v = '.'.join([str(i) for i in VERSION[:-1]])
    return '%s-%s' % (v, VERSION[-1])

__author__ = 'See the file AUTHORS.'
__license__ = 'GNU Lesser General Public License (GPL), Version 3'
__url__ = 'http://django-diario.googlecode.com'
__version__ = get_version()
