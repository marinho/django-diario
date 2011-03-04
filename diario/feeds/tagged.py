# -*- coding: utf-8 -*-
#
#  Copyright (c) 2007, 2008, 2009 Guilherme Gondim and contributors
#
#  This file is part of Django Diário.
#
#  Django Diário is free software under terms of the GNU Lesser
#  General Public License version 3 (LGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#

from django.contrib.syndication.feeds import Feed
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from diario.feeds.entries import RssEntriesFeed
from diario.models import Entry
from tagging.models import Tag

class RssEntriesByTagFeed(RssEntriesFeed):
    def get_object(self, bits):
        # In case of "rss/tags/example/foo/bar/", or other such
        # clutter, check that bits has only one member.
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Tag.objects.get(name__exact=bits[0])

    def title(self, tag):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _('%(title)s\'s Weblog: entries tagged "%(tag name)s"') % \
               {'title': self._site.name, 'tag name': tag.name}

    def description(self, tag):
        return _('Latest entries for tag "%(tag name)s"') % \
               {'tag name': tag.name}

    def link(self, tag):
        if not tag:
            raise FeedDoesNotExist
        return reverse('diario-tagged-entry-list', args=[tag.name])

    def get_query_set(self, tag):
        queryset = Entry.published_on_site.filter(tags__contains=tag.name)
        return queryset.order_by('-pub_date')

    def items(self, tag):
        return self.get_query_set(tag)[:15]

class AtomEntriesByTagFeed(RssEntriesByTagFeed):
    feed_type = Atom1Feed
    subtitle = RssEntriesByTagFeed.description
