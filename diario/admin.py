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

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from diario.models import Entry
from diario.settings import HAS_TAG_SUPPORT

if HAS_TAG_SUPPORT:
    TAG_FIELD = ['tags']
else:
    TAG_FIELD = []

class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    fieldsets = (
        (None, {
            'fields': ['title', 'slug', 'pub_date', 'body_source'] + TAG_FIELD
        }),
        (_('Status'), {
            'fields': ('is_draft', 'publish_on')
        }),
        (_('Discussion'), {
            'fields': ('enable_comments',)
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('markup',),
        })
    )
    list_display  = ('title', 'pub_date', 'author', 'is_draft',
                     'enable_comments')
    list_filter   = ('is_draft', 'publish_on', 'enable_comments', 'pub_date',
                     'markup')
    prepopulated_fields = {'slug': ('title',)}
    radio_fields = {'markup': admin.VERTICAL}
    search_fields = ['title', 'slug', 'body', 'author__username',
                     'author__first_name', 'author__last_name']

    def has_change_permission(self, request, obj=None):
        """
        Called from the individual object editing page, to ensure the
        user is allowed to edit that object.

        Returns ``True`` if the user has permission for change the
        entry, otherwise returns ``False``.
        """
        has_class_permission = super(EntryAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False
        return True

    def queryset(self, request):
        """
        Filter the entries based on ``request.user``. This only
        affects the entries shown in the list view.
        """
        if request.user.is_superuser:
            return Entry.objects.all()
        return Entry.objects.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        """
        Automatically fill in the author field on creation.
        """
        if not change:
            obj.author = request.user
        super(EntryAdmin, self).save_model(request, obj, form, change)

admin.site.register(Entry, EntryAdmin)
