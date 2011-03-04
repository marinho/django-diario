# -*- coding: utf-8 -*-
#
#  Copyright (c) 2009 Guilherme Gondim and contributors
#
#  This file is part of Django Diário.
#
#  Django Diário is free software under terms of the GNU Lesser
#  General Public License version 3 (LGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#

"""
URL definitions for weblog entries divided by author.
"""

from django.conf.urls.defaults import *
from diario.settings import DIARIO_NUM_LATEST

info_dict = {
    'paginate_by': DIARIO_NUM_LATEST,
    'template_name': 'diario/entry_list_by_author.html',
    'template_object_name': 'entry',
}

entry_list_by_author = url(        # entries by author
    regex  = '^(?P<author>[^/]+)/$',
    view   = 'diario.views.entries_by_author.entry_list_by_author',
    kwargs = info_dict,
    name   = 'diario-author-entry-list',
)

urlpatterns = patterns('', entry_list_by_author)
