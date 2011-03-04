# -*- coding: utf-8 -*-
#
#  Copyright (c) 2008, 2009 Guilherme Gondim and contributors
#
#  This file is part of Django Diário.
#
#  Django Diário is free software under terms of the GNU Lesser
#  General Public License version 3 (LGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#

from django.contrib.syndication import feeds
from django.http import Http404, HttpResponse

def feed(request, slug, bit='', feed_dict=None):
    """
    TODO: documment this.
    """
    if not feed_dict:
        raise Http404, "No feeds are registered."

    try:
        feed = feed_dict[slug]
    except KeyError:
        raise Http404, "Slug %r isn't registered." % slug

    try:
        feedgen = feed(slug, request).get_feed(bit)
    except feeds.FeedDoesNotExist:
        raise Http404, "Invalid feed parameters. Slug %r is valid, " % slug +\
                       "but bit, or lack thereof, are not."

    response = HttpResponse(mimetype=feedgen.mime_type)
    feedgen.write(response, 'utf-8')
    return response
