from django.db import models

# Create your models here.
class Feeds(models.Model):
    url=models.CharField(max_length=200)
    dateAdded=models.DateTimeField()
