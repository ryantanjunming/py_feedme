# (r'^accounts?/$','accounts.views.index'),
# (r'^accounts/(?i)login?/$','accounts.views.login'),
# (r'^accounts/(?i)logout?/$','accounts.views.logout'),
# (r'^accounts/(?i)register?/$','accounts.views.register'),
# (r'^accounts/(?i)profileView?/$','accounts.views.profileView'),
# (r'^accounts/(?i)profileSubmit?/$','accounts.views.profileSubmit'),

import os, sys, codecs, time
from datetime import datetime

# from django.core.context_processors import csrf
# from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
import socket
# from django.http import HttpResponse

import feedme.settings as settings

class BadAuthException(Exception):
    def __init__(self, msg):
        super(BadFeedException, self).__init__(msg)

def index(request):
    return render_to_response('accounts/index.html', 
    	context_instance=RequestContext(request))


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
				results = {'success' : True,
				'message' : 'Successful Login, you will be redirected',
				'redirect' : '/feeds/myFeeds/' }
			else:
				results = {'success' : False,
				'message' : 'Account has been disabled'}
	json = simplejson.dumps(results)
	return HttpResponse(json, mimetype='application/json')
