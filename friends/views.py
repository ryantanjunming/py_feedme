# Create your views here.

from django.contrib.auth.models import User
from friendship.models import Friend, Follow

def my_view(request):
    # List of this user's friends
    all_friends = Friend.objects.friends(request.user)

    # List all unread friendship requests
    requests = Friend.objects.unread_requests(user=request.user)

    # List all rejected friendship requests
    rejects = Friend.objects.rejected_requests(user=request.user)

    # List all sent friendship requests
    sent = Friend.objects.sent_requests(user=request.user)

    # List of this user's followers
    all_followers = Following.objects.followers(request.user)

    # List of who this user is following
    following = Following.objects.following(request.user)

    ### Managing friendship relationships
    other_user = User.objects.get(pk=1)
    new_relationship = Friend.objects.add_friend(request.user, other_user)
    Friend.objects.are_friends(request.user, other_user) == True
    Friend.objects.remove_friend(other_user, request.user)

    # Create request.user follows other_user relationship
    following_created = Following.objects.add_follower(request.user, other_user)