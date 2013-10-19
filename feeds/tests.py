"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from feeds.models import *
from friendship.models import Friend
from datetime import datetime

from recommend import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class RecommendationTest(TestCase):
    
    def create_user(self, username, first_name="John", last_name="Doe", email="DummyBS", password="IRDC"):
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        return user
    
    def test_friend_pref_recs(self):
        u0 = self.create_user("xxAznBladeIMSOCOOLDWABOUTITxx")
        u1 = self.create_user("SwagLord2000-1")
        u2 = self.create_user("CantThinkOfAGoodUsername")
        
        feeds = []
        for i in range(5): # 0 - 4
            name = "Feed_" + str(i) 
            feeds.append(Feeds.objects.create(name = name,
                                              url = name + ".com",
                                              dateAdded = datetime.now()))

        SubscribesTo.objects.create(user = u0,
                                    feed = feeds[0])
        SubscribesTo.objects.create(user = u0,
                                    feed = feeds[1])
        
        SubscribesTo.objects.create(user = u1,
                                    feed = feeds[3])
        SubscribesTo.objects.create(user = u1,
                                    feed = feeds[4])
        
        SubscribesTo.objects.create(user = u2,
                                    feed = feeds[0])
        SubscribesTo.objects.create(user = u2,
                                    feed = feeds[3])
        
        self.assertTrue(friend_pref_recommendations(u0) == None)
        
        rec_feeds = user_pref_recommendations(u0, threshold=0)
        self.assertTrue(len(rec_feeds) == 2, "Expected length: {}".format(len(rec_feeds)))
        self.assertTrue(rec_feeds[0] == feeds[3].pk)
        self.assertTrue(rec_feeds[1] == feeds[4].pk)
        
        # u0 is friends with both u1 and u2
        rel = Friend.objects.add_friend(u0, u1)
        rel.accept()
        rel = Friend.objects.add_friend(u0, u2)
        rel.accept()
        
        rec_feeds = friend_pref_recommendations(u0)
        self.assertTrue(len(rec_feeds) == 3)
        self.assertTrue(rec_feeds[0] == feeds[3].pk)
        possible_feeds = [feeds[0].pk, feeds[4].pk]
        self.assertTrue(rec_feeds[1] in possible_feeds)
        possible_feeds.remove(rec_feeds[1])
        self.assertTrue(rec_feeds[2] in possible_feeds)
        
        rec_feeds = user_pref_recommendations(u0, threshold=0)
        self.assertTrue(len(rec_feeds) == 2, "Expected length: {}".format(len(rec_feeds)))
        self.assertTrue(rec_feeds[0] == feeds[3].pk)
        self.assertTrue(rec_feeds[1] == feeds[4].pk)
        
        SubscribesTo.objects.create(user = u2,
                                    feed = feeds[2])
        
        # now u2 has feeds 0, 2, 3, and u1 has feeds 3, 4 - out of these, u0 only has feed 0
        # since u2 shares feed 0 with u0, feeds 3 and 2 should rank higher than 4
        # (remember these numbers aren't necessarily their PKs)
        rec_feeds = user_pref_recommendations(u0, threshold=0)
        self.assertTrue(len(rec_feeds) == 3, "Expected length: {}".format(len(rec_feeds)))
        possible_feeds = [feeds[3].pk, feeds[2].pk] # u1 doesn't share feeds with u0 - expecting 2 and 3 to have same score
        self.assertTrue(rec_feeds[0] in possible_feeds)
        possible_feeds.remove(rec_feeds[0])
        self.assertTrue(rec_feeds[1] in possible_feeds)
        self.assertTrue(rec_feeds[2] == feeds[4].pk)