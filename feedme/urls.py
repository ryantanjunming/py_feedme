from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


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
    
    (r'^accounts?/$','accounts.views.index'),
    (r'^accounts/(?i)login?/$','accounts.views.login'),
    # (r'^accounts/(?i)logout?/$','accounts.views.logout'),
    # (r'^accounts/(?i)register?/$','accounts.views.register'),
    # (r'^accounts/(?i)profileView?/$','accounts.views.profileView'),
    # (r'^accounts/(?i)profileSubmit?/$','accounts.views.profileSubmit'),

    
    (r'^feeds?/$','feeds.views.index'),
    (r'^feeds/(?i)myFeeds?/$','feeds.views.myFeeds'),
    (r'^feeds/(?i)insertFeed?/$','feeds.views.insertFeed'),
    (r'^feeds/(?i)deleteFeed?/$','feeds.views.deleteFeed'),
    (r'^feeds/(?i)insertRecommendation?/$','feeds.views.insertRecommendation'),
    (r'^feeds/(?i)deleteRecommendation?/$','feeds.views.deleteRecommendation'),
    (r'^feeds/(?i)showfeed?/$', 'feeds.views.showFeed'),
    (r'^feeds/(?i)billStripeToken?/$','feeds.views.billStripeToken'),
    (r'^feeds/(?i)feederror?/$', TemplateView.as_view(template_name="feeds/feederror.html"))
)
