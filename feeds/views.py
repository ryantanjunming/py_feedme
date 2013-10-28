# coding: utf-8
import os, sys, codecs, time
from datetime import datetime
from collections import OrderedDict

from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import *
from django.utils import simplejson

import feedparser
import stripe
import feedme.settings as settings

import pprint

from feeds.models import Feeds, SubscribesTo, FCategory, HasRead
from feeds.models import Recommendations
from django.core.exceptions import ObjectDoesNotExist
from recommend import *

from django.core.mail import EmailMessage



class BadFeedException(Exception):
    def __init__(self, msg):
        super(BadFeedException, self).__init__(msg)

def insert(insertURL, user):
    """
    Adds Feeds record corresponding to insertURL, and SubscribesTo record for
    the feed and given user.
    """
    feed = feedparser.parse(insertURL)
    if hasattr(feed, "bozo_exception") and feed['bozo_exception'].message == "syntax error":
        if settings.DEBUG: 
            print "Something bozo happened:", feed['bozo_exception']
            debug_feed_display(feed)
        raise BadFeedException("Error occured while trying to insert feed. Please check input URL.")
    try:
        feedname = feed['feed']['title']
    except:
        feedname = insertURL
    # if feed already exists, fetch that one and set to f
    try:
        f = Feeds.objects.get(url = str(insertURL).lower())
    except:
        f = Feeds(name = feedname,
                  url = str(insertURL).lower(),
                  dateAdded = datetime.now())
        f.save()
    subscribe = SubscribesTo(user = user, feed = f)
    subscribe.save()

def insertR(insertURL,insertSender,insertReceiver):
    feed = feedparser.parse(insertURL)
    if hasattr(feed, "bozo_exception") and feed['bozo_exception'].message == "syntax error":
        if settings.DEBUG: print "Something bozo happened:", feed['bozo_exception']
        raise BadFeedException("Error occured while trying to make recommendation. Please check input feed URL.")
    try:
        feedname = feed['feed']['title']
    except:
        feedname = insertURL
    r = Recommendations(name = str(feedname),
                        url = str(insertURL),
                        sender = str(insertSender),
                        receiver = str(insertReceiver))
    r.save()

def delete(deleteURL):
    f = Feeds.objects.get(url = str(deleteURL))
    f.delete()

def deleteR(deleteURL):
    r = Recommendations.objects.get(url = str(deleteURL))
    r.delete()

"""
================== CREATE YOUR VIEWS HERE ==================
"""
@login_required(login_url='/accounts/index/')
def index(request):
    return render_to_response('feeds/index.html', RequestContext(request))


@login_required(login_url='/accounts/index/')
def insertFeed(request):
    #print request.POST['feedurl']
    try:
        if request.method == "POST":
            insert(request.POST['feedurl'], request.user)
            return redirect("/feeds/myFeeds/")
        elif request.method == "GET":
            qkey, qvalue = request.META['QUERY_STRING'].split('=')
            if qkey == "url":
                insert(qvalue,request.user)
            return redirect("/feeds/myFeeds/")
    except BadFeedException as e:
        return redirect("/feeds/feederror/")

@login_required(login_url='/accounts/index/')
def insertFeedFromRecommendation(request):
    #print request.POST['feedurl']
    try:
        if request.method == "POST":
            insert(request.POST['feedurl'], request.user)
            return deleteRecommendation(request)
        elif request.method == "GET":
            qkey, qvalue = request.META['QUERY_STRING'].split('=')
            if qkey == "url":
                insert(qvalue,request.user)
            return deleteRecommendation(request)
    except BadFeedException as e:
        return redirect("/feeds/feederror/")

@login_required(login_url='/accounts/index/')
def insertRecommendation(request): # NOTE: it makes more sense for sender to be request.user!
    try:
        insertR(request.POST['feedurl'],request.user,request.POST['receiver'])
        return redirect("/feeds/myFeeds")
    except (BadFeedException):
        return redirect("/feeds/feederror")

@login_required(login_url='/accounts/index/')
def deleteRecommendation(request):
    if request.method == "POST":
        deleteR(request.POST['feedurl'])
    elif request.method == "GET":
        qkey, qvalue = request.META['QUERY_STRING'].split('=')
        if qkey == "url":
            deleteR(qvalue)
    return redirect("/feeds/myFeeds")

@login_required(login_url='/accounts/index/')
def myFeeds(request):
    # populating my current rss feeds
    feed_entries = get_categorised_feeds(request.user)
    host_site = request.META['HTTP_HOST']
    for cat in feed_entries:
        feed_entries[cat] = map(lambda feed: {'url' : feed.url, 
                                              'name' : feed.name,
                                              'del_url' : "http://"+ host_site + "/feeds/deleteFeed?url=" + feed.url
                                              }, 
                                feed_entries[cat])
    # populating my current recommendations
    rec_entries = []
    for r in selectAllR(request.user.username):
        rec_entries.append({'url' : r.url,
                            'name' : r.name,
                            'add_url' : "http://"+ host_site + "/feeds/insertFeedFromRecommendation?url=" + r.url,
                            'del_url' : "http://"+ host_site + "/feeds/deleteRecommendation?url=" + r.url
                            })
    # friend preference recommendation
    f_prefs = friend_pref_recommendations(request.user)[:3]
    f_prefs = Feeds.objects.filter(pk__in=f_prefs) # pks to Feeds objects
    f_prefs = map(lambda feed: {'url' : feed.url, 
                                'name' : feed.name,
                                'add_url' : "http://"+ host_site + "/feeds/insertFeed?url=" + feed.url,
                                'del_url' : "http://"+ host_site + "/feeds/deleteFeed?url=" + feed.url
                                },
                  f_prefs) 
    # user preference
    user_recs = user_pref_recommendations(request.user)[:3]
    user_recs = Feeds.objects.filter(pk__in=user_recs) # pks to Feeds objects
    user_recs = map(lambda feed: {'url' : feed.url, 
                                  'name' : feed.name,
                                  'add_url' : "http://"+ host_site + "/feeds/insertFeed?url=" + feed.url,
                                  'del_url' : "http://"+ host_site + "/feeds/deleteFeed?url=" + feed.url
                                  }, 
                    user_recs)
    # rendering the page
    t = loader.get_template('feeds/myFeeds.html')
    c = RequestContext(request, {
        'feed_entries' : feed_entries,
        'rec_entries' : rec_entries,
        'friend_recs' : f_prefs,
        'user_recs' : user_recs,
        'username' : request.user.username
    })
    return render_to_response('feeds/myFeeds.html', c)

@login_required
def mark_entry_read(request):
    entry_url = request.GET.get('url', None)
    if not entry_url: return redirect("/feeds/myFeeds")
    mark = HasRead(user = request.user,
                   entry = entry_url)
    mark.save()
    return redirect("/feeds/myFeeds")

@login_required(login_url='/accounts/index/')
def deleteFeed(request):
    if request.method == "POST":
        delete(request.POST['feedurl'])
    elif request.method == "GET":
        qkey, qvalue = request.META['QUERY_STRING'].split('=')
        if qkey == "url":
            delete(qvalue)
    return redirect("/feeds/myFeeds")


# NOTE: we really need a shortcut for a delayed redirect view (display input message + auto redirect in 3 seconds kind of thing - maybe a template will help)
# (if we can use a template for this, will be super good for the feed error page, since I'm currently using a generic error page...)

def get_categorised_feeds(user):
    """
    For the given user, returns a dict of
        category_name : [Feed, Feed, Feed, ...]
    Corresponding to the user's categories and their Feeds in the categories.
    Feeds without categories default to the category name "Cat-less".
    """
    categories = OrderedDict({'Cat-less' : []})
    for feed in select_feed_by_user(user.pk):
        # grab all FCategorys that feed belongs to
        feed_cats = FCategory.objects.filter(feed = feed)
        if feed_cats:
            # add feed to each of its category listings
            for cat in feed_cats:
                if not categories.has_key(cat.cat_name): categories[cat.cat_name] = []
                categories[cat.cat_name].append(feed)
        else:
            # default listing
            categories['Cat-less'].append(feed)
    return categories

@login_required(login_url='/accounts/index/')
def categorise_feed(request):
    """
    For current user, processes query string and adds feed to given category.
    Assumes the form
        /feeds/categorise?name=cat_name&url=feed_url
        where feed_url corresponds to a feed that the user is subscribed to
    """
    cat_name, feed_url = request.GET.get('name', None), request.GET.get('url', None) # TODO Check for invalid?
    if not (cat_name and feed_url):
        print "Bad query values", cat_name, feed_url
        return redirect("/feeds/feederror/")
    feed_url = feed_url.lower()
    try:
        feed = Feeds.objects.get(url = feed_url)
    except ObjectDoesNotExist:
        print "Tried to fetch a Feeds object that doesn't exist! UserID:", request.user.pk, "Feed url:", feed_url
        return redirect("/feeds/feederror/")
    c = FCategory(user = request.user,
                  feed = feed,
                  cat_name = cat_name)
    c.save()
    return redirect("/feeds/myFeeds")

@login_required(login_url='/accounts/index/')
def category_delete(request):
    """
    Used for deleting categories, from query string. Has two modes:
        /feeds/catdel?delete=category&name=cat_name                deletes category with name cat_name
        /feeds/catdel?delete=feed&name=cat_name&url=feed_url       deletes feed from given cat_name 
    """
    # TODO should check for invalid query strings
    del_type = request.GET.get('delete', None)
    cat_name = request.GET.get('name', None) # remember this is case sensitive!
    if del_type == "category" and cat_name:
        # delete category records with given cat_name
        FCategory.objects.filter(cat_name = cat_name).delete()
    elif del_type == "feed" and cat_name:
        feed_url = request.GET.get('url', None)
        if feed_url:
            try:
                # delete all category records linked with feeds that have the url feed_url
                FCategory.objects.filter(feed = Feeds.objects.get(url = feed_url)).delete()
            except ObjectDoesNotExist:
                print "Tried to fetch a Feeds object that doesn't exist! UserID:", request.user.pk, "Feed url:", feed_url
                return redirect("/feeds/feederror/")
    return redirect("/feeds/myFeeds")


"""Some nice utility stuff"""

#select all Feeds
def selectAll():
    allfeeds = Feeds.objects.all()
    return allfeeds

def select_feed_by_user(user_id):
    """Selects all Feeds that the given user_id subscribes to."""
    # get list of IDs of the Feeds that user_id subscribes to
    feed_ids = SubscribesTo.objects.filter(user = user_id)
    feed_ids = map(lambda subscribe: subscribe.feed.pk, feed_ids)
    # use list of IDs to fetch the Feeds
    return Feeds.objects.filter(pk__in=feed_ids)

#select all Recommendations
def selectAllR(username):
    allrec = Recommendations.objects.filter(receiver=username)
    return allrec


# NOTE: apparently using the request metadata can be dangerous 
# - http://stackoverflow.com/questions/1451138/how-can-i-get-the-domain-name-of-my-site-within-a-django-template
# def showFeed(request):
#     # CURRENTLY ONLY SUPPORTS ONE KEY=VALUE IN QUERY STRING (and doesn't even care what the key is!)
#     # but please use 'url' as key
#     qkey, qvalue = request.META['QUERY_STRING'].split('=')
#     url = qvalue
#     feed = feedparser.parse(url)
#     if settings.DEBUG: debug_feed_display(feed)
#     return HttpResponse(make_feed_page(feed, request.META['HTTP_HOST'], request.user))

def showFeed(request):
    # CURRENTLY ONLY SUPPORTS ONE KEY=VALUE IN QUERY STRING (and doesn't even care what the key is!)
    # but please use 'url' as key
    url = request.POST.get('url')
    feed = feedparser.parse(url)
    tile = int(request.POST.get('tile'))
    
    return HttpResponse(make_feed_json(feed, request.META['HTTP_HOST'], request.user, tile), mimetype='application/json')

# some feed display functions (will prob move to another file later)
def debug_feed_display(feed, show_entries=0):
    """
    Prints string representation of the feed's contents, for debugging purposes.
    """
    sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout, errors='replace')
    print ">>> Displaying feed <<< "
    for k in feed.keys():
        if k != "entries" and k != "feed": 
            print ">>", k, ":", feed[k]
    print "> Displaying feed['feed']"
    for k in feed['feed'].keys():
        print ">>", k, ":", feed['feed'][k]
    for _ in range(show_entries):
        print "> Displaying feed['entries']"
        for entry in feed['entries']:
            print ">> Entry start"
            for k in entry.keys():
                print ">>>", k, ":", entry[k]
    print ">>> Finished displaying feed <<< \n"

def make_feed_page(feed, host_site, user=None):
    """
    Returns HTML (string) for displaying the feed object given.
    feed should be the returned value from feedparser.parse
    """
    try:
        img = feed['feed']['icon']
    except (KeyError):
        try:
            img = feed['feed']['image']['href']
        except (KeyError):
            img = "IMG"
    title_icon = "<img src=\"" + img + "\">"
    title_header = "<h2><a href=\"" + feed['feed']['link'] + "\" target=\"_blank\">" + feed['feed']['title'] + "</a></h2>" + \
                   "<a href=\"" + feed['feed']['link'] + "\" target=\"_blank\">" + title_icon + "</a>"
    
    updated_time = "Last Updated: "
    last_updated = "(Time not found!)"
    # note: I actually don't know if this is accurate... or how to grab timezone info
    try:
        last_updated = datetime.fromtimestamp(time.mktime(feed['feed']['updated_parsed']))
    except (KeyError):
        try:
            last_updated = datetime.fromtimestamp(time.mktime(feed['updated_parsed']))
        except (KeyError):
            pass
    updated_time += str(last_updated)
    feed_header = title_header + "<br>" + updated_time

    entries = ""
    #tried to use addthis for each feed entry, Failed
    for entry in feed['entries']:
        if user and \
                HasRead.objects.filter(user=user, entry=entry['link']).exists(): # don't display feeds the user has marked as read
            continue
        entries += "<hr>" + make_entry_string(entry, host_site)
    if entries:
        page = feed_header + "<br>" + entries.decode('utf-8')
    else:
        page = feed_header + "<br>All entries read!."
    return page


def make_feed_json(feed, host_site, user, tile):
    """
    Does the same things as make_feed_page but in json
    """
    try:
        img = feed['feed']['icon']
    except (KeyError):
        try:
            img = feed['feed']['image']['href']
        except (KeyError):
            img = "IMG"

    
    updated_time = "Last Updated: "
    last_updated = "(Time not found!)"
    # note: I actually don't know if this is accurate... or how to grab timezone info
    try:
        last_updated = datetime.fromtimestamp(time.mktime(feed['feed']['updated_parsed']))
    except (KeyError):
        try:
            last_updated = datetime.fromtimestamp(time.mktime(feed['updated_parsed']))
        except (KeyError):
            pass
    updated_time += str(last_updated)
    
    pp = pprint.PrettyPrinter(indent=2)

    request_entries = []
    start = tile*20
    end = start+20
    for i in range(start, end):
        entry = feed['entries'][i]
        fields = {'link' : entry.link,
                    'title' : entry.title,
                    'author' : "No Author" if not entry.author else entry.author,
                    'published' : str(datetime.fromtimestamp(time.mktime(entry['published_parsed']))),
                    'markreadlink' : host_site + "/feeds/markRead?url=" + entry.link,
                    'summary' : entry.summary,
                    'content' : entry.content
                }

        request_entries.append(fields)

    # pp.pprint(request_entries);
    # print('<<<<<<<<<<<<<<<<<< >>>>>>>>>>>>>>>>>>>>>');
    
    responseObject = { 
            'title_icon' : img,
            'title_link' : feed['feed']['link'],
            'title_title' : feed['feed']['title'],
            'last_updated' : updated_time,
            'request_entries' : request_entries
            }
    
    # pp.pprint(responseObject)
    
    json = simplejson.dumps(responseObject)
    
    return json


def make_entry_string(entry, host_site):
    """
    From feedparser.parse(url)['entries'] objects, returns HTML string
    to display an entry.
    """
    fields = {'link' : entry['link'],
              'title' : entry['title'],
              'author' : "No Author" if not entry.has_key('author') else entry['author'],
              'published' : str(datetime.fromtimestamp(time.mktime(entry['published_parsed']))),
              'markreadlink' : host_site + "/feeds/markRead?url=" + entry['link'],
              'summary' : entry['summary']}
    #added custom facebook share button
    for k in fields.keys():
        fields[k] = fields[k].encode('utf-8')
    return "<div><h3><a href=\"{link}\" target=\"_blank\">{title}</a></h3>{author}, \
published on {published}<br><a href=\"{markreadlink}\">Mark as Read</a><br>{summary}<br></div>".format(**fields)+\
"""<br><button href="#" 
  onclick="
    window.open(
      'http://www.facebook.com/sharer/sharer.php?s=100&p[url]={link}&p[images][0]=&p[title]={title}&p[summary]={title}', 
      'facebook-share-dialog', 
      'width=626,height=436'); 
    return false;" style="color:white;background-color:#3B5998">
  Share on Facebook
</button>""".format(**fields)+\
"""
<a href="https://twitter.com/share" class="twitter-share-button" data-lang="en" data-url="{link}" data-text="{title}">Tweet</a>
""".format(**fields)+\
"""
<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="https://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
"""
#bugs page
def bugs(request):
    return render_to_response('feeds/bugs.html', context_instance=RequestContext(request))

def sentBugs(request):
    msg = EmailMessage('You have Bugs!.. in your room..',request.POST.get('bugs') , to=['hljw4@hotmail.com'])#to=['mefeeed@gmail.com'])
    msg.send()
    return render_to_response('feeds/sentBugs.html', context_instance=RequestContext(request))

#payment system below
#magic do not touch
def billStripeToken(request):
    # Set your secret key: remember to change this to your live secret key in production
    # See your keys here https://manage.stripe.com/account
    stripe.api_key = "sk_test_eCmqaN318lcvnTskneiJhPoj"

    # Get the credit card details submitted by the form
    token = request.POST['stripeToken']

    # Create the charge on Stripe's servers - this will charge the user's card
    try:
        charge = stripe.Charge.create(
		amount=1000, # amount in cents, again
        currency="usd",
        card=token,
        description="payinguser@example.com"
    )
    except stripe.CardError, e:
        # The card has been declined
        pass
    return redirect("/feeds/myFeeds")

