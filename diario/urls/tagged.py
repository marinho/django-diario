# -*- coding: utf-8 -*-
#
#  Copyright (c) 2008 Guilherme Mesquita Gondim and contributors
#
#  This file is part of Django Diário.
#
#  Django Diário is free software under terms of the GNU Lesser
#  General Public License version 3 (LGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#

"""
URL definitions for weblog entries divided by tag.
"""

from django.conf.urls.defaults import *
from diario.settings import DIARIO_NUM_LATEST

info_dict = {
    'paginate_by': DIARIO_NUM_LATEST,
    'template_name': 'diario/entry_list_tagged.html',
    'template_object_name': 'entry',
}

tagged_entry_list = url(        # entries by tag
    regex  = '^(?P<tag>[^/]+)/$',
    view   = 'diario.views.tagged.tagged_entry_list',
    kwargs = info_dict,
    name   = 'diario-tagged-entry-list',
)

urlpatterns = patterns('', tagged_entry_list)
