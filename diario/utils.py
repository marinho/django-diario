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

from xmlrpclib import ServerProxy

def markuping(markup, value):
    """
    Transform plain text markup syntaxes to HTML with filters in
    django.contrib.markup.templatetags.

    *Required arguments:*

        * ``markup``: 'markdown', 'rest' or 'texttile'. For any other string
                    value is returned without modifications.
        * ``value``: plain text input

    """
    if markup == 'markdown':
        from markdown import markdown
        return markdown(value)
    elif markup == 'rest':
        from django.contrib.markup.templatetags.markup import restructuredtext
        return restructuredtext(value)
    elif markup == 'textile':
        from django.contrib.markup.templatetags.markup import textile
        return textile(value)
    else:
        return value            # raw

def ping_weblog_directory(site_name, site_url, server_url, fail_silently=True):
    """
    Ping weblog directory about weblog updates. Works with Technorati,
    ping-o-matic and others.

    *Required arguments:*

        * ``site_name``: name of site/weblog.
        * ``site_url``: site/weblog URL.
        * ``server_url``: URL of XML-RPC server to ping.

    *Optional arguments:*

        * ``fail_silently``: if true, don't raises any exception when
                           ping fails.

    Note: In signals module you have a signal to ping ping-o-matic.
    """
    server = ServerProxy(server_url)
    try:
        return server.weblogUpdates.ping(site_name, site_url)
    except Exception, e:
        if fail_silently:
            return
        raise e
