# Create your views here.

from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import *

from django.contrib.auth.models import User
from friendship.models import Friend

@login_required(login_url='/accounts/index')
def my_view(request):

    # List of this user's friends
    user = request.user
    print user
    all_friends = Friend.objects.friends(user)
    

    # List all unread friendship requests
    #requests = Friend.objects.unread_requests(user=request.user)

    # List all rejected friendship requests
    #rejects = Friend.objects.rejected_requests(user=request.user)

    # List all sent friendship requests
    #sent = Friend.objects.sent_requests(user=request.user)

    # List of this user's followers
    #all_followers = Following.objects.followers(request.user)

    # List of who this user is following
    #following = Following.objects.following(request.user)

    ### Managing friendship relationships
    #other_user = User.objects.get(pk=1)
    #new_relationship = Friend.objects.add_friend(request.user, other_user)
    #Friend.objects.are_friends(request.user, other_user) == True
    #Friend.objects.remove_friend(other_user, request.user)

    # Create request.user follows other_user relationship
    #following_created = Following.objects.add_follower(request.user, other_user)
 
    c = RequestContext(request, {
        'friends' : str(all_friends)
     #   'friend_requests' : requests
        #'friend_recs' : f_prefs,
        #'user_recs' : user_recs,
        #'username' : request.user.username
    })

    return render_to_response('friends/index.html', c)
    
