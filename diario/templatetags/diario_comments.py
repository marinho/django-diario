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
The ``diario.templatetags.diario_comments`` module defines a number of
template tags which may be used to work with comments.

To access Diário comments template tags in a template, use the {% load %}
tag::

    {% load diario_comments %}
"""

from django import template
from django.conf import settings
from django.contrib.comments.models import Comment

register = template.Library()

class CommentListNode(template.Node):
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
        get_list_function = Comment.objects.filter
        kwargs = {
            'is_public': True,
            'is_removed': False,
            'site__pk': settings.SITE_ID,
            'content_type__app_label__exact': 'diario',
            'content_type__model__exact': 'entry',
        }
        comment_list = get_list_function(**kwargs).select_related().order_by('-submit_date')
        context[self.var_name] = comment_list[self.start:][:self.num]
        return ''

def do_get_diario_comment_list(parser, token):
    """
    Gets Diário's comment list and populates the template context with a
    variable containing that value, whose name is defined by the 'as' clause.

    Syntax::

        {% get_diario_comment_list [num] (from the [start]) as [var_name] %}

    Example usage to get latest comments::

        {% get_diario_comment_list 10 as latest_diario_comments %}

    To get old comments::

        {% get_diario_comment_list 10 from the 10 as old_comments %}

    To get previous comments from the last comment on page with
    ``last_on_page`` context variable provided by ``object_list``, do::

        {% get_diario_comment_list 10 from the last_on_page as old_comments %}

    Note: The start point is omitted.
    """
    bits = token.contents.split()
    if len(bits) == 4:
        if bits[2] != 'as':
            raise template.TemplateSyntaxError, "Second argument to '%s' tag must be 'as'" % bits[0]
        return CommentListNode(bits[1], bits[3])
    if len(bits) == 7:
        if bits[2] != 'from' or bits[3] != 'the':
            raise template.TemplateSyntaxError, "Second and third arguments to '%s' tag must be 'from the'" % bits[0]
        if bits[5] != 'as':
            raise template.TemplateSyntaxError, "Fifth argument to '%s' tag must be 'as'" % bits[0]
        return CommentListNode(bits[1], bits[6], bits[4])
    else:
        raise template.TemplateSyntaxError, "'%s' tag takes three or six arguments" % bits[0]

register.tag('get_diario_comment_list', do_get_diario_comment_list)
