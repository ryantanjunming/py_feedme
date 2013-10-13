import os, sys, codecs, time
from datetime import datetime

from django.core.context_processors import csrf
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import *

import feedparser
import stripe
import feedme.settings as settings

from feeds.models import Feeds
from feeds.models import Recommendations


class BadFeedException(Exception):
    def __init__(self, msg):
        super(BadFeedException, self).__init__(msg)

def insert(insertURL):
    feed = feedparser.parse(insertURL)
    if hasattr(feed, "bozo_exception"):
        raise BadFeedException("Error occured while trying to insert feed. Please check input URL.")
    try:
        feedname = feed['feed']['title']
    except:
        feedname = insertURL
    f = Feeds(name = feedname,
              url = str(insertURL),
              dateAdded = datetime.now())
    f.save()

def insertR(insertURL,insertSender,insertReceiver):
    feed = feedparser.parse(insertURL)
    if hasattr(feed, "bozo_exception"):
        raise BadFeedException("Error occured while trying to insert feed. Please check input URL.")
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
def index(request):
    
    

    return render_to_response('feeds/index.html', RequestContext(request))



def insertFeed(request):
    #print request.POST['feedurl']
    try:
        insert(request.POST['feedurl'])
        return redirect("/feeds/myFeeds/")
    except (BadFeedException):
        return redirect("/feeds/feederror/")

def insertRecommendation(request):
    try:
        insertR(request.POST['feedurl'],request.POST['sender'],request.POST['receiver'])
        return redirect("/feeds/myFeeds")
    except (BadFeedException):
        return redirect("/feeds/feederror")

def deleteRecommendation(request):
    if request.method == "POST":
        deleteR(request.POST['feedurl'])
    elif request.method == "GET":
        qkey, qvalue = request.META['QUERY_STRING'].split('=')
        if qkey == "url":
            deleteR(qvalue)
    return redirect("/feeds/myFeeds")

def myFeeds(request):

    #populating my current rss feeds
    ret_str = ""
    for feed in selectAll():
        #Jackie I've changed the one line below will it affect anything else? like the del_link_tag
        ret_str += "<li><button type=\"button\" value=\"" + "http://"+ request.META['HTTP_HOST'] + "/feeds/showfeed?url=" + feed.url + "\" target=\"_blank\">" + feed.name + "</button>"
        # delete icon
        del_img = '<img src="{imgsrc}" alt="Delete Button" width="16" height="16">'
        del_img = del_img.format(imgsrc = os.path.join("/static", "img", "delete.png"))
        del_link_tag = "<a href=\"" + "http://"+ request.META['HTTP_HOST'] + "/feeds/deleteFeed?url=" + feed.url + "\">"
        ret_str += " " + del_link_tag + del_img + "</a></li>"
    
    #populating my current recommendations
    myRecommendations_str = ""
    for r in selectAllR():
        myRecommendations_str += "<li><button type=\"button\" value=\"" + "http://"+ request.META['HTTP_HOST'] + "/feeds/showfeed?url=" + r.url + "\" target=\"_blank\">" + r.name + "</button>"
        # delete icon
        del_img = '<img src="{imgsrc}" alt="Delete Button" width="16" height="16">'
        del_img = del_img.format(imgsrc = os.path.join("/static", "img", "delete.png"))
        del_link_tag = "<a href=\"" + "http://"+ request.META['HTTP_HOST'] + "/feeds/deleteRecommendation?url=" + r.url + "\">"
        myRecommendations_str += " " + del_link_tag + del_img + "</a></li>"
    
    #rendering the page
    t=loader.get_template('feeds/myFeeds.html')
    c=RequestContext(request,{
        'myFeeds':ret_str,
        'recommendations':myRecommendations_str
    })
    return render_to_response('feeds/myFeeds.html', c)
    

def deleteFeed(request):
    if request.method == "POST":
        delete(request.POST['feedurl'])
    elif request.method == "GET":
        qkey, qvalue = request.META['QUERY_STRING'].split('=')
        if qkey == "url":
            delete(qvalue)
    return redirect("/feeds/myFeeds")

#select all Feeds
def selectAll():
    allfeeds = Feeds.objects.all()
    return allfeeds

#select all Recommendations
def selectAllR():
    allrec = Recommendations.objects.all()
    return allrec


# NOTE: apparently using the request metadata can be dangerous 
# - http://stackoverflow.com/questions/1451138/how-can-i-get-the-domain-name-of-my-site-within-a-django-template
def showFeed(request):
    # CURRENTLY ONLY SUPPORTS ONE KEY=VALUE IN QUERY STRING (and doesn't even care what the key is!)
    # but please use 'url' as key
    qkey, qvalue = request.META['QUERY_STRING'].split('=')
    url = qvalue
    feed = feedparser.parse(url)
    if settings.DEBUG: debug_feed_display(feed)
    return HttpResponse(make_feed_page(feed))



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
    


def make_feed_page(feed):
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
    title_header = "<h2><a href=\"" + feed['feed']['link'] + "\">" + feed['feed']['title'] + "</a></h2>" + \
                   "<a href=\"" + feed['feed']['link'] + "\">" + title_icon + "</a>"
    
    updated_time = "Last Updated: "
    # note: I actually don't know if this is accurate... or how to grab timezone info
    last_updated = "(Time not found!)"
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
    for entry in feed['entries']:
        entries += "<hr>" + make_entry_string(entry)
            
    page = feed_header + "<br>" + entries.decode('utf-8')
    return page


def make_entry_string(entry):
    """
    From feedparser.parse(url)['entries'] objects, returns HTML string
    to display an entry.
    """
    fields = {'link' : entry['link'],
              'title' : entry['title'],
              'author' : entry['author'],
              'published' : str(datetime.fromtimestamp(time.mktime(entry['published_parsed']))),
              'summary' : entry['summary']}
    for k in fields.keys():
        fields[k] = fields[k].encode('utf-8')
    return "<h3><a href=\"{link}\">{title}</a></h3>{author}, published on {published}<br>{summary}".format(**fields)
    


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
