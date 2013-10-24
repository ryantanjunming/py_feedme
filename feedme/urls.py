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
   # (r'','accounts.views.index'),

    
    (r'^accounts?/$','accounts.views.index'),
    (r'^accounts/(?i)index?/$','accounts.views.index'),
    (r'^accounts/(?i)login?/$','accounts.views.login'),
    (r'^accounts/(?i)logout?/$','accounts.views.logout'),
    (r'^accounts/(?i)register?/$','accounts.views.register'),
    
    (r'^accounts/(?i)resetPassword?/$','accounts.views.resetPassword'),
    (r'^accounts/(?i)resetPasswordP?/$','accounts.views.resetPasswordP'),
    # (r'^accounts/(?i)profileView?/$','accounts.views.profileView'),
    # (r'^accounts/(?i)profileSubmit?/$','accounts.views.profileSubmit'),

    
    (r'^feeds?/$','feeds.views.index'),
    (r'^feeds/(?i)myFeeds?/$','feeds.views.myFeeds'),
    (r'^feeds/(?i)insertFeed?/$','feeds.views.insertFeed'),
    (r'^feeds/(?i)insertFeedFromRecommendation?/$','feeds.views.insertFeedFromRecommendation'),
    (r'^feeds/(?i)deleteFeed?/$','feeds.views.deleteFeed'),
    (r'^feeds/(?i)insertRecommendation?/$','feeds.views.insertRecommendation'),
    (r'^feeds/(?i)deleteRecommendation?/$','feeds.views.deleteRecommendation'),
    (r'^feeds/(?i)showfeed?/$', 'feeds.views.showFeed'),
    (r'^feeds/(?i)billStripeToken?/$','feeds.views.billStripeToken'),
    (r'^feeds/(?i)feederror?/$', TemplateView.as_view(template_name="feeds/feederror.html")),
    (r'^feeds/(?i)categorise?/$','feeds.views.categorise_feed'),
    (r'^feeds/(?i)catdel?/$','feeds.views.category_delete'),

    (r'^friends?/$','friends.views.my_view'),
    (r'^friends/(?i)add?/$','friends.views.add_friend'),
    (r'^friends/(?i)remove?/$','friends.views.remove_friend'),
    (r'^friends/(?i)accept?/$','friends.views.accept_friendship'),
    (r'^friends/(?i)reject?/$','friends.views.reject_friendship'),
    (r'^friends/(?i)cancel?/$','friends.views.cancel_request')

)
