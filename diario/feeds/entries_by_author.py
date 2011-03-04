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
from django.contrib.syndication.feeds import Feed
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from diario.feeds.entries import RssEntriesFeed
from diario.models import Entry

class RssEntriesByAuthorFeed(RssEntriesFeed):
    def get_object(self, bits):
        # In case of "rss/authors/example/foo/bar/", or other such
        # clutter, check that bits has only one member.
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return User.objects.get(username__exact=bits[0])

    def title(self, user):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _('%(title)s\'s Weblog: entries by "%(user name)s"') % \
               {'title': self._site.name, 'user name': user.username}

    def description(self, user):
        return _('Latest entries by "%(user name)s"') % \
            {'user name': user.username}

    def link(self, user):
        if not user:
            raise FeedDoesNotExist
        return reverse('diario-author-entry-list', args=[user.username])

    def get_query_set(self, user):
        queryset = Entry.published_on_site.filter(author=user)
        return queryset.order_by('-pub_date')

    def items(self, user):
        return self.get_query_set(user)[:15]

class AtomEntriesByAuthorFeed(RssEntriesByAuthorFeed):
    feed_type = Atom1Feed
    subtitle = RssEntriesByAuthorFeed.description
