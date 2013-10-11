from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'feedme.views.home', name='home'),
    # url(r'^feedme/', include('feedme.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    

    (r'^feeds/$','feeds.views.index'),
    (r'^feeds/(?i)myFeeds$','feeds.views.myFeeds'),
    (r'^feeds/insertFeed$','feeds.views.insertFeed'),
    (r'^feeds/deleteFeed$','feeds.views.deleteFeed'),
    (r'^feeds/(?i)showfeed$', 'feeds.views.showFeed'),
    (r'^feeds/(?i)billStripeToken$','feeds.views.billStripeToken')
)
