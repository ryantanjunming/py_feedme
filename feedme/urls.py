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
    (r'^accounts/login?/$','accounts.views.login'),
    (r'^accounts/loginSubmit?/$','accounts.views.login'),
    (r'^accounts/logout?/$','accounts.views.logout'),
    (r'^accounts/register?/$','accounts.views.register'),
    (r'^accounts/registerSubmit?/$','accounts.views.register'),
    (r'^accounts/viewProfile?/$','accounts.views.viewProfile'),

    
    (r'^feeds?/$','feeds.views.index'),
    (r'^feeds/(?i)myFeeds?/$','feeds.views.myFeeds'),
    (r'^feeds/insertFeed?/$','feeds.views.insertFeed'),
    (r'^feeds/deleteFeed?/$','feeds.views.deleteFeed'),
    (r'^feeds/insertRecommendation?/$','feeds.views.insertRecommendation'),
    (r'^feeds/deleteRecommendation?/$','feeds.views.deleteRecommendation'),
    (r'^feeds/(?i)showfeed?/$', 'feeds.views.showFeed'),
    (r'^feeds/(?i)billStripeToken?/$','feeds.views.billStripeToken'),
    (r'^feeds/(?i)feederror?/$', TemplateView.as_view(template_name="feeds/feederror.html"))
)
