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
The ``diario.templatetags.diario_entries`` module defines a number of
template tags which may be used to work with entries.

To access Diário entries template tags in a template, use the {% load %}
tag::

    {% load diario_entries %}
"""

from django import template
from diario.models import Entry

register = template.Library()

class MonthListNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = list(Entry.published_on_site.dates("pub_date", "month", order="DESC"))
        return ''

def do_get_diario_month_list(parser, token):
    """Gets month list that have entries and populates the template context
    with a variable containing that value, whose name is defined by the 'as'
    clause.

    Syntax::

        {% get_diario_month_list as [var_name] %}

    Example usage::

        {% get_diario_month_list as archive %}

        {% get_diario_month_list as blog_months %}
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "'%s' tag takes three arguments" % bits[0]
    if bits[1] != 'as':
        raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
    return MonthListNode(bits[2])


class EntryListNode(template.Node):
    def __init__(self, num, var_name, start=0):
        try:
            self.start = int(start)
        except ValueError:
            self.start =  template.Variable(start)
        self.num = int(num)
        self.var_name = var_name

    def render(self, context):
        if type(self.start) != int:
            try:
                self.start =  int(self.start.resolve(context))
            except template.VariableDoesNotExist:
                return ''
        context[self.var_name] = Entry.published_on_site.all()[self.start:][:self.num]
        return ''

def do_get_diario_entry_list(parser, token):
    """
    Gets entries list and populates the template context with a variable
    containing that value, whose name is defined by the 'as' clause.

    Syntax::

        {% get_diario_entry_list [num] (from the [start]) as [var_name] %}

    Example usage to get latest entries::

        {% get_diario_entry_list 10 as latest_entries %}

    To get old entries::

        {% get_diario_entry_list 10 from the 10 as old_entries %}

    To get previous entries from the last entry on page with ``last_on_page``
    context variable provided by ``object_list`` view, do::

        {% get_diario_entry_list 10 from the last_on_page as old_entries %}

    Note: The start point is omitted.
    """
    bits = token.contents.split()
    if len(bits) == 4:
        if bits[2] != 'as':
            raise template.TemplateSyntaxError, "Second argument to '%s' tag must be 'as'" % bits[0]
        return EntryListNode(bits[1], bits[3])
    if len(bits) == 7:
        if bits[2] != 'from' or bits[3] != 'the':
            raise template.TemplateSyntaxError, "Third and fourth arguments to '%s' tag must be 'from the'" % bits[0]
        if bits[5] != 'as':
            raise template.TemplateSyntaxError, "Fifth argument to '%s' tag must be 'as'" % bits[0]
        return EntryListNode(bits[1], bits[6], bits[4])
    else:
        raise template.TemplateSyntaxError, "'%s' tag takes three or seven arguments" % bits[0]


register.tag('get_diario_entry_list', do_get_diario_entry_list)
register.tag('get_diario_month_list', do_get_diario_month_list)
