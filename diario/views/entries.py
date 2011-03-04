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

from django.views.generic import date_based, list_detail
from diario.models import Entry

def entry_detail(request, *args, **kwargs):
    """
    A wrapper around ``django.views.generic.date_based.object_detail``
    which creates a ``QuerySet`` containing drafts and future entries
    if user has permission to change entries
    (``diario.change_entry``).

    This is useful for preview entries with your own templates and
    CSS.

    Tip: Uses the *View on site* button in Admin interface to access
    yours drafts and entries in future.
    """
    kwargs['date_field'] = 'pub_date'
    kwargs['slug_field'] = 'slug'
    if request.user.has_perm('diario.change_entry'):
        kwargs['allow_future'] = True
        kwargs['queryset'] = Entry.on_site.all()
    else:
        kwargs['allow_future'] = False
        if 'queryset' not in kwargs:
            kwargs['queryset'] = Entry.published_on_site.all()
    return date_based.object_detail(request, *args, **kwargs)

def entry_archive_year(request, *args, **kwargs):
    """
    A thin wrapper around ``django.views.generic.date_based.archive_year``.
    """
    kwargs['date_field'] = 'pub_date'
    if 'queryset' not in kwargs:
        kwargs['queryset'] = Entry.published_on_site.all()
    return date_based.archive_year(request, *args, **kwargs)

def entry_archive_month(request, *args, **kwargs):
    """
    A thin wrapper around ``django.views.generic.date_based.archive_month``.
    """
    kwargs['date_field'] = 'pub_date'
    if 'queryset' not in kwargs:
        kwargs['queryset'] = Entry.published_on_site.all()
    return date_based.archive_month(request, *args, **kwargs)

def entry_archive_day(request, *args, **kwargs):
    """
    A thin wrapper around ``django.views.generic.date_based.archive_day``.
    """
    kwargs['date_field'] = 'pub_date'
    if 'queryset' not in kwargs:
        kwargs['queryset'] = Entry.published_on_site.all()
    return date_based.archive_day(request, *args, **kwargs)

def entry_list(request, *args, **kwargs):
    """
    A thin wrapper around ``django.views.generic.list_detail.object_list``.
    """
    if 'queryset' not in kwargs:
        kwargs['queryset'] = Entry.published_on_site.all()
    return list_detail.object_list(request, *args, **kwargs)
