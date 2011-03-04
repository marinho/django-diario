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

from django.contrib.auth.models import User
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic import list_detail

from diario.models import Entry

def entry_list_by_author(request, author=None, *args, **kwargs):
    """
    A thin wrapper around ``django.views.generic.list_detail.object_list``.

    In addition to the context variables set up by ``object_list``, a
    ``author`` context variable will contain the ``User`` instance for the
    entry author.
    """
    if author is None:
        try:
            author = kwargs.pop('author')
        except KeyError:
            raise AttributeError(_('entry_list_by_author must be called with '
                                   'a author.'))
    try:
        user_instance = User.objects.get(username=author)
    except User.DoesNotExist:
        raise Http404(_('No User found matching "%s".') % author)
    if 'queryset' not in kwargs:
        kwargs['queryset'] = Entry.published_on_site
    kwargs['queryset'] = kwargs['queryset'].filter(author=user_instance)
    if 'extra_context' not in kwargs:
        kwargs['extra_context'] = {}
    kwargs['extra_context']['author'] = user_instance
    return list_detail.object_list(request, *args, **kwargs)
