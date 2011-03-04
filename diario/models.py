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

"""
Models definitions for Diário.
"""

from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _

from diario.managers import PublishedManager, CurrentSitePublishedManager
from diario.settings import DIARIO_DEFAULT_MARKUP_LANG, HAS_TAG_SUPPORT


MARKUP_CHOICES = (
    ('markdown', 'Markdown'),
    ('rest',     'reStructuredText'),
    ('textile',  'Textile'),
    ('raw',      _('Raw text')),
)

if HAS_TAG_SUPPORT:
    from tagging.fields import TagField

class Entry(models.Model):
    """A weblog entry."""

    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(
        _('slug'),
        unique_for_date='pub_date',
        help_text=_('Automatically built from the title. A slug is a short '
                    'label generally used in URLs.'),
    )
    author = models.ForeignKey(User, editable=False, verbose_name=_('author'))
    body_source = models.TextField(_('body'))
    body = models.TextField(
        _('body in HTML'),
        blank=True,
        editable=False,
    )
    markup = models.CharField(
        _('markup language'),
        default=DIARIO_DEFAULT_MARKUP_LANG,
        max_length=8,
        choices=MARKUP_CHOICES,
        help_text=_('Select "Raw text" to enter HTML or apply markup '
                    'elsewhere.'),
    )
    is_draft = models.BooleanField(
        _('draft'),
        default=False,
        help_text=_('Drafts are not published.'),
    )
    pub_date = models.DateTimeField(
        _('date published'),
        default=datetime.now,
        help_text=_('Entries in future dates are only published on '
                    'correct date.'),
    )
    publish_on = models.ManyToManyField(
        Site,
        default=[settings.SITE_ID],
        verbose_name=_('publish on')
    )
    enable_comments = models.BooleanField(_('enable comments'), default=True)

    if HAS_TAG_SUPPORT:
        tags = TagField(blank=True)

    # managers
    objects   = models.Manager()
    published = PublishedManager()
    on_site   = CurrentSiteManager('publish_on')
    published_on_site = CurrentSitePublishedManager('publish_on')

    class Meta:
        get_latest_by = 'pub_date'
        ordering      = ('-pub_date',)
        verbose_name  = _('entry')
        verbose_name_plural = _('entries')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('diario-entry', None, {
            'year' : str(self.pub_date.year),
            'month': str(self.pub_date.month).zfill(2),
            'day'  : str(self.pub_date.day).zfill(2),
            'slug' : str(self.slug)
        })
    get_absolute_url = permalink(get_absolute_url)

    def in_future(self):
        return self.pub_date > datetime.now()


from django.db.models import signals
from diario.signals import convert_body_to_html, update_draft_date
signals.pre_save.connect(convert_body_to_html, sender=Entry)
signals.pre_save.connect(update_draft_date, sender=Entry)
