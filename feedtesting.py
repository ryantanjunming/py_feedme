import feedparser

pythonUrl="http://feeds.gawker.com/kotaku/full"

feed = feedparser.parse(pythonUrl)

for i in feed["items"]:
    if "summary" in i:
        print i["summary"]
        break

