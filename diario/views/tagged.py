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

from tagging.views import tagged_object_list
from diario.models import Entry

def tagged_entry_list(request, *args, **kwargs):
    """
    A thin wrapper around ``tagging.views.tagged_object_list``.
    """
    if 'queryset_or_model' not in kwargs:
        kwargs['queryset_or_model'] = Entry.published_on_site.all()
    return tagged_object_list(request, *args, **kwargs)
