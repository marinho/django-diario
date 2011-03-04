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
Default Diário application settings.

If you not configure the settings below in your own project settings.py,
they assume default values::

    DIARIO_DEFAULT_MARKUP_LANG
        Markup language for blog entries. Options: 'rest', 'textile',
        'markdown' or 'raw' for raw text.
        Default: 'raw'.

    DIARIO_NUM_LATEST
        Number of latest itens on object_list view. Default: 10.
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_app

#
#  (!!!)
#
#  DON'T EDIT THESE VALUES, CONFIGURE IN YOUR OWN PROJECT settings.py
#

DIARIO_DEFAULT_MARKUP_LANG = getattr(settings, 'DIARIO_DEFAULT_MARKUP_LANG',
                                     'raw')
DIARIO_NUM_LATEST = getattr(settings, 'DIARIO_NUM_LATEST', 10)


# django-tagging support
try:
    get_app('tagging')
    HAS_TAG_SUPPORT = True
except ImproperlyConfigured:
    HAS_TAG_SUPPORT = False
