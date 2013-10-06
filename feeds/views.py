from django.template import Context,loader
from django.http import HttpResponse
#from feeds.models import Feeds

# Create your views here.
def index(request):
    t=loader.get_template('feeds/index.html')
    c=Context({
        'lover':'Jack'
    })	
    return HttpResponse(t.render(c))

