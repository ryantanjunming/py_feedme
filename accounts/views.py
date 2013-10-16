# (r'^accounts/(?i)profileView?/$','accounts.views.profileView'),
# (r'^accounts/(?i)profileSubmit?/$','accounts.views.profileSubmit'),

import os, sys, codecs, time, hashlib, random
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core.mail import EmailMessage
from django.db.models.signals import post_save

import socket
# from django.http import HttpResponse

import feedme.settings as settings


class BadAuthException(Exception):
    def __init__(self, msg):
        super(BadAuthException, self).__init__(msg)

def index(request):
	if(request.user.is_authenticated()):
		return redirect("/feeds/myFeeds/")
	else:
		return render_to_response('accounts/index.html', context_instance=RequestContext(request))
    	


def login(request):
	results = {'success' : False,
				'message' : 'Username and Password were incorrect'}

	if request.POST.get('formType') == "login":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			# the password verified for the user
			if user.is_active:
				auth_login(request, user)
				results = {'success' : True,
				'message' : 'Successful Login, Welcome <strong>'+user.get_full_name()+'</strong>',
				'redirect' : '/feeds/myFeeds/' }
			else:
				results = {'success' : False,
				'message' : 'Account has been disabled'}
	json = simplejson.dumps(results)
	return HttpResponse(json, mimetype='application/json')


def logout(request):
    auth_logout(request)
    return redirect("/accounts/")


def register(request):
	results = {'success' : False,
				'message' : 'Whoops, something went wrong' }

	if request.POST.get('formType') == "register":
		
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')

		# try:
		user = User.objects.create_user(username, email, password)		
		user.first_name = first_name
		user.last_name = last_name
		user.is_active = True
		user.save();

		# except:
		# 	results = {
		# 			'success' : False,
		# 			'message' : 'Registration Unsucessful'
		# 		}
		# 	json = simplejson.dumps(results)
		# 	return HttpResponse(json, mimetype='application/json')

		# profile = user.get_profile()
		# m = hashlib.md5()
		# m = m.update(random.random())
		# profile.auth_key = m.hexdigest()
		# profile.save()

		msg = EmailMessage('Registration to FeedMe.','Hi, you have successfully registered for FeedMe.', to=[user.email])
		msg.send()
		
		print("ive reached here")

		results = {'success' : True,
				'message' : 'Successful Registration, Welcome <strong>'+user.get_full_name()+'</strong>',
				'redirect' : '/feeds/myFeeds/' }
				

	json = simplejson.dumps(results)
	return HttpResponse(json, mimetype='application/json')

# To handle changes with the DB and fields
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.\
                 objects.get_or_create(user=instance)
post_save.connect(create_profile, sender=User)