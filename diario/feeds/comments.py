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

from django.conf import settings
from django.contrib.comments.models import Comment
from django.contrib.syndication.feeds import Feed
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from diario.models import Entry

class RssCommentsFeed(Feed):
    """All weblog comments RSS feeds.
    """
    description = _('Latest comments on Weblog')
    title_template = 'feeds/comments_title.html'
    description_template = 'feeds/comments_description.html'

    def title(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _("%(title)s's Weblog comments") % \
               {'title': self._site.name}

    def link(self):
        return reverse('diario-entry-list')

    def item_pubdate(self, comment):
        return comment.submit_date

    def get_query_set(self):
        get_list_function = Comment.objects.filter
        kwargs = {
            'is_public': True,
            'site__pk': settings.SITE_ID,
            'content_type__app_label__exact': 'diario',
            'content_type__model__exact': 'entry',
        }
        return get_list_function(**kwargs).order_by('-submit_date')

    def items(self):
        return self.get_query_set()[:30]

class AtomCommentsFeed(RssCommentsFeed):
    """All weblog comments Atom feeds.
    """
    feed_type = Atom1Feed
    subtitle = RssCommentsFeed.description

class RssCommentsByEntryFeed(RssCommentsFeed):
    """Comments RSS feeds for a specific entry.
    """
    def get_object(self, bits):
        # In case of "rss/weblog/1/foo/bar/", or other such clutter, check that
        # bits has only one member.
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Entry.objects.get(id=bits[0])

    def title(self, entry):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _("Comments on: %(entry title)s @ %(weblog title)s's Weblog") %\
            {'entry title':  entry.title, 'weblog title': self._site.name}

    def description(self, entry):
        return _('Latest comments for "%(title)s"') % {'title': entry.title}

    def link(self, entry):
        if not entry:
            raise FeedDoesNotExist
        return reverse('diario-entry', kwargs={
            'year' : str(entry.pub_date.year),
            'month': str(entry.pub_date.month).zfill(2),
            'day'  : str(entry.pub_date.day).zfill(2),
            'slug' : str(entry.slug)
        })

    def item_author_name(self, comment):
        return comment.user_name

    def item_author_link(self, comment):
        return comment.user_url

    def get_query_set(self, entry):
        get_list_function = Comment.objects.filter
        kwargs = {
            'is_public': True,
            'site__pk': settings.SITE_ID,
            'content_type__app_label__exact': 'diario',
            'content_type__model__exact': 'entry',
            'object_pk': entry.id
        }
        return get_list_function(**kwargs).order_by('-submit_date')

    def items(self, entry):
        return self.get_query_set(entry)[:30]

class AtomCommentsByEntryFeed(RssCommentsByEntryFeed):
    """Comments Atom feeds for a specific entry.
    """
    feed_type = Atom1Feed
    subtitle = RssCommentsByEntryFeed.description
