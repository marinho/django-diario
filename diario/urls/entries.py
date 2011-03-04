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
URL definitions for weblog entries.
"""

from django.conf.urls.defaults import *
from diario.settings import DIARIO_NUM_LATEST

info_dict = {
    'template_object_name': 'entry',
}

entry_detail = url(
    regex  = '^(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
    view   = 'diario.views.entries.entry_detail',
    kwargs = dict(info_dict, month_format='%m'),
    name   = 'diario-entry'
)

archive_day = url(
    regex  = '^(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\d{2})/$',
    view   = 'diario.views.entries.entry_archive_day',
    kwargs = dict(info_dict, month_format='%m'),
    name   = 'diario-archive-day'
)

archive_month = url(
    regex  = '^(?P<year>\d{4})/(?P<month>[0-9]{2})/$',
    view   = 'diario.views.entries.entry_archive_month',
    kwargs = dict(info_dict, month_format='%m'),
    name   = 'diario-archive-month'
)

archive_year = url(
    regex  = '^(?P<year>\d{4})/$',
    view   = 'diario.views.entries.entry_archive_year',
    kwargs = info_dict,
    name   = 'diario-archive-year'
)

entry_list = url(
    regex  = '^$',
    view   = 'diario.views.entries.entry_list',
    kwargs = dict(info_dict, paginate_by=DIARIO_NUM_LATEST),
    name   = 'diario-entry-list'
)

urlpatterns = patterns('', entry_detail, archive_day, archive_month,
                       archive_year, entry_list)
