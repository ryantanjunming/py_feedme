from django.template import Context,loader
from django.http import HttpResponse
import feedparser
#from feeds.models import Feeds

# Create your views here.
def index(request):
    t=loader.get_template('feeds/index.html')
    c=Context({
        'lover':'Jack'
    })	
    return HttpResponse(t.render(c))

def feedTest(request):
    pythonUrl="http://feeds.gawker.com/kotaku/full"
    feed = feedparser.parse(pythonUrl)
    for i in feed["items"]:
        if "summary" in i:
            return HttpResponse(i["summary"])
            break
    

    








