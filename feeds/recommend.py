from __future__ import division

from django.contrib.auth.models import User
from friendship.models import Friend
from feeds.models import Feeds, SubscribesTo

# okay these are definitely bugged

def user_pref_recommendations(user, threshold=0.01):
    """
    Given a User, returns a list of integers corresponding to the PKs of
    Feeds objects, sorted by score in descending order.
    
    Score is determined by examining the user's subscribed feeds, and comparing
    that with the feeds of other users to predict what other feeds the given user
    may be interested in (the assumption is that two users with overlapping
    subscribed feeds have similar interests).
    
    The resulting list won't contain feeds that the user has subscribed to.
    You should probably check that the user given has at least a few feeds before
    calling this function.
    """
    jc_threshold = threshold
    # construct sets corresponding to the feeds that each user is subscribed to
    sub_feeds = {user.pk : set()}
    for sub in SubscribesTo.objects.select_related():
        if not sub_feeds.has_key(sub.user.pk): sub_feeds[sub.user.pk] = set()
        sub_feeds[sub.user.pk].add(sub.feed.pk)
    # the algorithm doesn't assign score for a given user's feeds if jc == 0 for that set and the user's set
    # so we could check for emptiness in user's set and quit here if we want ... not too much difference tho
    
    # use similarity between sets to score feeds
    feed_scores = {}
    for upk in sub_feeds.iterkeys():
        # compute the Jaccard Coefficient for the given user and each other user for
        # their sets of subscribed feeds
        if upk != user.pk:
            inter_set = sub_feeds[upk].intersection(sub_feeds[user.pk])
            jc = len(inter_set) / len(sub_feeds[upk].union(sub_feeds[user.pk]))
            # if similarity exceeds jc_thresh,
            # for each feed that the other user has that the given user does not have,
            # accumulate score, weighted by jc similarity
            if jc >= jc_threshold:
                for feedpk in sub_feeds[upk] - inter_set:
                    if not feed_scores.has_key(feedpk): feed_scores[feedpk] = 0
                    feed_scores[feedpk] += float(1) * jc # I don't think the float is necessary, but I've had some bad experiences...
    # make a list of feed pks, sorted by their score (descending)
    return sorted(feed_scores.iterkeys(),
                  key = lambda k: feed_scores[k],
                  reverse = True)
    
def friend_pref_recommendations(user):
    """
    Given a User, returns a list of integers corresponding to the PKs of
    Feeds objects, sorted by score in descending order, or None if the User
    has no friends.
    
    Score is determined by examining the user's registered friends and their
    subscribed feeds, such that the highest scoring feed is the most popular
    feed among the given user's friends.
    
    Returned list includes feeds that the user is subscribed to.
    """
    # get a list of pks corresponding to given user's friends
    friends = map(lambda f: f.pk, Friend.objects.friends(user))
    if not friends: return [] # skip out if user has no friends
    feed_scores = {}
    # accumulate score for feeds that the given user's friends are subscribed to
    for sub in SubscribesTo.objects.select_related().filter(user__in=friends):
        if not feed_scores.has_key(sub.feed.pk): feed_scores[sub.feed.pk] = 0
        feed_scores[sub.feed.pk] += 1
    # return list of feed pks, sorted by score in descending order
    return sorted(feed_scores.iterkeys(),
                  key = lambda k: feed_scores[k],
                  reverse = True)
