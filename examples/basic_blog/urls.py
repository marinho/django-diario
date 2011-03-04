from django.conf.urls.defaults import *
from django.contrib import admin
from diario.feeds.entries import RssEntriesFeed, AtomEntriesFeed
from diario.feeds.tagged import RssEntriesByTagFeed, AtomEntriesByTagFeed

admin.autodiscover()

entries_feeds = {
    'rss': RssEntriesFeed,
    'atom': AtomEntriesFeed,
}

entries_by_tag_feeds = {
    'rss': RssEntriesByTagFeed,
    'atom': AtomEntriesByTagFeed,
}

urlpatterns = patterns('',
    # homepage
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'flatfiles/homepage.html'}),

    # weblog
    (r'^weblog/', include('diario.urls.entries')),
    (r'^weblog/(?P<slug>(rss|atom))/$', 'diario.views.syndication.feed', {'feed_dict': entries_feeds}),

    # admin
    (r'^admin/(.*)', admin.site.root),
)
