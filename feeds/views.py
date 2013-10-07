from django.template import Context,loader
from django.http import HttpResponse
import feedparser
from feeds.models import Feeds

# Create your views here.
def index(request):
    t=loader.get_template('feeds/index.html')
    c=Context({
        'lover':'Jack'
    })	
    return HttpResponse(t.render(c))

def feedTest(request):
    pythonUrl="http://www.theverge.com/rss/frontpage"
    feed = feedparser.parse(pythonUrl)
    for i in feed["entries"]:
        if "summary" in i:
            return HttpResponse(i["summary"])
            break

def insert(insertURL, date)
    f = Feeds(url = "{}".format(insertURL)
             dateAdded = datetime.datetime.now())
    f.save()

import sys, codecs
import time
from datetime import datetime

def feedTestRoar(request):
    # so i can print out the debug msgs without exploding
    sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout, errors='replace')
    url = "http://feeds.feedburner.com/RockPaperShotgun"
    #url = "http://www.theverge.com/rss/frontpage"
    #url = "http://kotaku.com/vip.xml"
    feed = feedparser.parse(url)
    for k in feed.keys():
        if k != "entries": print ">>", k, ":", feed[k]
    for k in feed['feed'].keys():
        print ">>", k, ":", feed['feed'][k]
    return HttpResponse(make_feed_page(feed))

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
    try:
        last_updated = datetime.fromtimestamp(time.mktime(feed['feed']['updated_parsed']))
    except (KeyError):
        last_updated = datetime.fromtimestamp(time.mktime(feed['updated_parsed']))
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
##    entry = ("<h2>" + "<a href=\"" + entry['link'] + "\">" + entry['title'] + "</a></h2>" # linked heading
##             str(entry['author'])
##             ", updated " + str(datetime.fromtimestamp(time.mktime(entry['updated_parsed']))) + ""
##             "<br>" + entry['summary']
##             )
    return "<h3><a href=\"{link}\">{title}</a></h3>{author}, published on {published}<br>{summary}".format(**fields)
    
