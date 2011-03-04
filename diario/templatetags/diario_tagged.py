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
The ``diario.templatetags.diario_tagged`` module defines a number of
template tags which may be used to work with entries tags.

To access this template tags in a template, use the {% load %}
tag::

    {% load diario_tagged %}
"""
from django.template import Library
from tagging.templatetags.tagging_tags import do_tag_cloud_for_model

register = Library()

def do_tag_cloud_for_entries(parser, token):
    """
    A wrapper around ``tagging.templatetags.do_tag_cloud_for_model``
    which add a filter to exclude draft entries from ``QuerySet``.

    This template tag retrieves a list of ``Tag`` objects for a Entry
    model, with tag cloud attributes set, and stores them in a context
    variable.

    Usage::

       {% tag_cloud_for_entries as [varname] %}

    Extended usage::

       {% tag_cloud_for_entries as [varname] with [options] %}

    Extra options can be provided after an optional ``with`` argument,
    with each option being specified in ``[name]=[value]`` format. Valid
    extra options are:

       ``steps``
          Integer. Defines the range of font sizes.

       ``min_count``
          Integer. Defines the minimum number of times a tag must have
          been used to appear in the cloud.

       ``distribution``
          One of ``linear`` or ``log``. Defines the font-size
          distribution algorithm to use when generating the tag cloud.

    Examples::

       {% tag_cloud_for_entries as entries_tags %}
       {% tag_cloud_for_entries as entries_tags with steps=9 min_count=3 distribution=log %}

    """
    token.contents = token.contents.replace(
        'tag_cloud_for_entries',
        'tag_cloud_for_model diario.Entry',
        1
    )
    node = do_tag_cloud_for_model(parser, token)
    node.kwargs['filters'] = {'is_draft': False}
    return node

register.tag('tag_cloud_for_entries', do_tag_cloud_for_entries)
