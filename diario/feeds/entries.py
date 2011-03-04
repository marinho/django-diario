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

from django.conf import settings
from django.contrib.syndication.feeds import Feed
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext as _

from diario.models import Entry

class RssEntriesFeed(Feed):
    description = _('Latest entries on Weblog')
    title_template = 'feeds/diario_title.html'
    description_template = 'feeds/diario_description.html'

    def title(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _("%(title)s's Weblog") % {'title': self._site.name}

    def link(self):
        return reverse('diario-entry-list')

    def get_query_set(self):
        return Entry.published_on_site.order_by('-pub_date')

    def items(self):
        return self.get_query_set()[:15]

    def item_author_name(self, entry):
        if entry.author.get_full_name():
            return entry.author.get_full_name()
        return entry.author.username

    def item_author_email(self, entry):
        if entry.author.email:
            return entry.author.email

    def item_author_link(self, entry):
        try:
            return reverse('diario-author-entry-list',
                           args=[entry.author.username])
        except NoReverseMatch:
            pass

    def item_pubdate(self, entry):
        return entry.pub_date

    def item_categories(self, entry):
        try:
            return entry.tags.split()
        except AttributeError:
            pass      # ignore if not have django-tagging support

class AtomEntriesFeed(RssEntriesFeed):
    feed_type = Atom1Feed
    subtitle = RssEntriesFeed.description
