import os, sys, codecs, time
from datetime import datetime

from django.core.context_processors import csrf
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect

import feedparser
import stripe

import feedme.settings as settings
from feeds.models import Feeds


def insert(insertURL):
    feed = feedparser.parse(insertURL)
    try:
        feedname = feed['feed']['title']
    except:
        feedname = insertURL
    f = Feeds(name = feedname,
              url = str(insertURL),
              dateAdded = datetime.now())
    f.save()

def delete(deleteURL):
    f = Feeds.objects.get(url = str(deleteURL))
    f.delete()

# Create your views here.
def index(request):
    t=loader.get_template('feeds/index.html')
    c=RequestContext(request,{
        'lover':'Jack'
    })	
    return HttpResponse(t.render(c))

#is this still used?
def addFeed(request):
    pythonUrl="http://feeds.gawker.com/kotaku/full"
    feed = feedparser.parse(pythonUrl)
    t=loader.get_template('feeds/feedTest.html')
    c=RequestContext(request,{
        'lala':'land'
    })
    return HttpResponse(t.render(c))

def insertFeed(request):
    #print request.POST['feedurl']
    insert(request.POST['feedurl'])
    return HttpResponseRedirect("/feeds/myFeeds")

def myFeeds(request):
    ret_str = ""
    for feed in selectAll():
        ret_str += "<li><a href=\"" + "http://"+ request.META['HTTP_HOST'] + "/feeds/showfeed?url=" + feed.url + "\" target=\"_blank\">" + feed.name + "</a>"
        # delete icon
        del_img = '<img src="{imgsrc}" alt="Delete Button" width="16" height="16">'
        del_img = del_img.format(imgsrc = os.path.join("..", "static", "img", "delete.png"))
        del_link_tag = "<a href=\"" + "http://"+ request.META['HTTP_HOST'] + "/feeds/deleteFeed?url=" + feed.url + "\">"
        ret_str += " " + del_link_tag + del_img + "</a></li>"
    t=loader.get_template('feeds/myFeeds.html')
    c=RequestContext(request,{
        'lover':ret_str
    })
    return HttpResponse(t.render(c))

def deleteFeed(request):
    if request.method == "POST":
        delete(request.POST['feedurl'])
    elif request.method == "GET":
        qkey, qvalue = request.META['QUERY_STRING'].split('=')
        if qkey == "url":
            delete(qvalue)
    return HttpResponseRedirect("/feeds/myFeeds")

def selectAll():
    allfeeds = Feeds.objects.all()
    return allfeeds

# NOTE: apparently using the request metadata can be dangerous - http://stackoverflow.com/questions/1451138/how-can-i-get-the-domain-name-of-my-site-within-a-django-template

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
    return HttpResponseRedirect("/feeds/myFeeds")
