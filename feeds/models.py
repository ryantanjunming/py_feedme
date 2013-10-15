from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Feeds(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    dateAdded = models.DateTimeField()

class SubscribesTo(models.Model):
    user = models.ForeignKey(User)
    feed = models.ForeignKey(Feeds)

class FCategory(models.Model):
    """
    A named category for different Feeds, e.g. "Music" for music related feeds.
    """
    user = models.ForeignKey(User)
    feed = models.ForeignKey(Feeds)
    cat_name = models.CharField(max_length=20)

class Recommendations(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    sender = models.CharField(max_length=200) #foreign key
    receiver = models.CharField(max_length=200)#foreign key
    #seen field unconfirmed, will implement when it comes to that.
