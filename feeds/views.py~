from django.template import Context,loader
from django.http import HttpResponse
import feedparser
from feeds.models import Feeds
from django.core.context_processors import csrf
from django.template import RequestContext
import sys, codecs
import time
from datetime import datetime

def insert(insertURL):
    f = Feeds(url = "{}".format(insertURL),dateAdded = datetime.now())
    f.save()


# Create your views here.
def index(request):
    t=loader.get_template('feeds/index.html')
    c=RequestContext({
        'lover':'Jack'
    })	
    return HttpResponse(t.render(c))

def feedTest(request):
    pythonUrl="http://feeds.gawker.com/kotaku/full"
    feed = feedparser.parse(pythonUrl)
    t=loader.get_template('feeds/feedTest.html')
    c=RequestContext(request,{
        'lala':'land'
    })
    return HttpResponse(t.render(c))
    #for i in feed["entries"]:
    #    if "summary" in i:
    #        return HttpResponse(i["summary"])
    #        break

def insertFeed(request):
    #print request.POST['feedurl']
    insert(request.POST['feedurl'])
    return HttpResponse("Thanks for the feed!")




def feedTestRoar(request):
    #sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout, errors='replace')
    url = "http://www.theverge.com/rss/frontpage"
    return HttpResponse(make_feed_page(feedparser.parse(url)))

# PLAN: write a func to display a feed in its entirety (return HttpResponse)
# includes writing something that constructs something to display each entry
# main problem: entries don't come with images consistently

def make_feed_page(feed):
    """
    Returns HTML (string) for displaying the feed object given.
    feed should be the returned value from feedparser.parse
    """
    title_icon = "<img src=\"" + feed['feed']['icon'] + "\">"
    title_header = feed['feed']['title'] + "<br>" + "<a href=\"" + feed['feed']['link'] + "\">" + title_icon + "</a>"
    
    updated_time = "Last Updated: "
    # note: I actually don't know if this is accurate... or how to grab timezone info
    last_updated = datetime.fromtimestamp(time.mktime(feed['feed']['updated_parsed']))
    updated_time += str(last_updated)

    feed_header = title_header + "<br>" + updated_time

    entries = ""

    for entry in feed['entries']:
        entries += "<hr>" + make_entry_string(entry)
            
    page = feed_header + "<br>" + entries
    return page

def make_entry_string(entry):
    """
    From feedparser.parse(url)['entries'] objects, returns HTML string
    to display an entry.
    """
    fields = {'link' : entry['link'],
              'title' : entry['title'],
              'author' : entry['author'],
              'updated' : str(datetime.fromtimestamp(time.mktime(entry['updated_parsed']))),
              'summary' : entry['summary']}
##    entry = ("<h2>" + "<a href=\"" + entry['link'] + "\">" + entry['title'] + "</a></h2>" # linked heading
##             str(entry['author'])
##             ", updated " + str(datetime.fromtimestamp(time.mktime(entry['updated_parsed']))) + ""
##             "<br>" + entry['summary']
##             )
    return "<h2><a href=\"{link}\">{title}</a></h2>{author}, updated at {updated}<br>{summary}".format(**fields)
    
