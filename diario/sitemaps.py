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

from django.contrib.sitemaps import Sitemap
from diario.models import Entry

class DiarioSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Entry.published_on_site.all()

    def lastmod(self, obj):
        return obj.pub_date
