# Create your views here.

from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import *

from django.contrib.auth.models import User
from friendship.models import Friend, FriendshipRequest

from friends.exceptions import AlreadyExistsError

@login_required(login_url='/accounts/index')
def my_view(request):

    # List of this user's friends
    all_friends = Friend.objects.friends(request.user)
    

    # List all unread friendship requests
    requests = Friend.objects.unread_requests(request.user)

    # List all users
    all_users = User.objects.all()
    

    # List all rejected friendship requests
    #rejects = Friend.objects.rejected_requests(user=request.user)

    # List all sent friendship requests
    sent = Friend.objects.sent_requests(user=request.user)

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
    t = loader.get_template('friends/index.html')
    c = RequestContext(request, {
        'friends' : all_friends,
        'friend_requests' : requests,
        'users' : all_users,
        'sent' : sent
        #'friend_recs' : f_prefs,
        #'user_recs' : user_recs,
        #'username' : request.user.usernase
    })

    return render_to_response('friends/index.html', c)
    #return HttpResponse(all_friends)

@login_required(login_url='/accounts/index/')
def add_friend(request):
    if request.method == 'POST':
       to_username = request.POST['username']
       to_user = User.objects.get(username = to_username)
       from_user = request.user
       try:
           Friend.objects.add_friend(from_user, to_user)
       except AlreadyExistsError as e:
           print "Already exists " + str(from_user) + " " + str(to_user) 
    return redirect("/friends/")


@login_required(login_url='/accounts/index/')
def remove_friend(request):
    other_user = User.objects.get(username = request.POST['username'])
    Friend.objects.remove_friend(request.user, other_user)
    return redirect("/friends/")

@login_required(login_url='/accounts/index/')
def accept_friendship(request):
    if request.method == 'POST':
        requestid = request.POST['rid']
        f_request = get_object_or_404(FriendshipRequest, id = requestid)
        f_request.accept()
    return redirect("/friends/")

@login_required(login_url='/accounts/index/')
def reject_friendship(request):
    if request.method == 'POST':
        requestid = request.POST['rid']
        f_request = get_object_or_404(FriendshipRequest, id = requestid)
        f_request.reject()
    return redirect("/friends/")
