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
Custom managers for Django models registered with Diário application.
"""

from datetime import datetime
from django.contrib.sites.managers import CurrentSiteManager
from django.db.models import Manager
from diario.settings import HAS_TAG_SUPPORT


class PublishedManager(Manager):
    """
    Manager for published entries on all sites. A published entry is
    non-draft and/or non-future entry.
    """

    def get_query_set(self):
        queryset = super(PublishedManager, self).get_query_set()
        return queryset.filter(is_draft=False, pub_date__lte=datetime.now)

    if HAS_TAG_SUPPORT:
        def tagged(self, tag_instance):
            """
            Returns a QuerySet for a tag.
            """
            from tagging.models import TaggedItem
            return TaggedItem.objects.get_by_model(self.get_query_set(),
                                                   tag_instance)

class CurrentSitePublishedManager(CurrentSiteManager):
    """
    Manager for published entries on current site. A published entry is
    non-draft and/or non-future entry.
    """

    def get_query_set(self):
        queryset = super(CurrentSitePublishedManager, self).get_query_set()
        return queryset.filter(is_draft=False, pub_date__lte=datetime.now)

    if HAS_TAG_SUPPORT:
        def tagged(self, tag_instance):
            """Returns a QuerySet for a tag.
            """
            from tagging.models import TaggedItem
            return TaggedItem.objects.get_by_model(self.get_query_set(),
                                                   tag_instance)
