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
Signals relating to entries.
"""

from datetime import datetime
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from diario.utils import markuping, ping_weblog_directory

def convert_body_to_html(instance, **kwargs):
    """
    Convert plain text markup in ``body_source`` field to HTML.

    This signal always connected in models module using ``pre_save``
    method.
    """
    instance.body = unicode(markuping(instance.markup,
                                      instance.body_source))

def update_draft_date(sender, instance, **kwargs):
    """
    Update instance's pub_date if entry was draft.

    This signal always connected in models module using ``pre_save``
    method.
    """
    try:
        e = sender.objects.get(id=instance.id)
        if e.is_draft:
            instance.pub_date = datetime.now()
    except sender.DoesNotExist:
        pass

def ping_with_pingomatic(instance, created, **kwargs):
    """
    Updates multiple services and search engines about updates to
    weblog content, with `ping-o-matic <http://pingomatic.com/>`_.

    To connect this signal, you need use ``post_save``
    method. Example::

      signals.post_save.connect(ping_with_pingomatic, sender=Entry)

    """
    if created:
        site = Site.objects.get_current()
        site_url = 'http://%s' % site + reverse('diario-entry-list')
        ping_weblog_directory(site.name, site_url, 'http://rpc.pingomatic.com/')
