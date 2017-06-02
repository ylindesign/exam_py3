from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse

from django.contrib import messages
from .models import Users

def index(request):
	if 'name' in request.session:
		return redirect('travel:travel')
	return render(request, 'login/index.html')

def register(request):
	person = {
		'name': request.POST['name'],
		'username': request.POST['username'],
		'password': request.POST['password'],
		'conf_pw': request.POST['conf_pw'],
	}

	if request.method != "POST":
		messages.add_message(request, messages.ERROR, "Cant have an empty form")
		return redirect("/")

	response = Users.objects.regis(person)

	if response['status'] == False:
		for error in response['errors']:
			messages.add_message(request, messages.ERROR, error)
		return redirect("/")
	else:
		messages.add_message(request, messages.SUCCESS, "You have registered!" )
		request.session['name'] = person['name']
		request.session['id'] = response['person'].id
	return redirect('travel:travel')

def login(request):
	if request.method != "POST":
		messages.add_message(request, messages.ERROR, "Must be logged in")
		return redirect('/')
	# print "name: ", len(request.POST['email_login'])
	# print "pw: ", len(request.POST['pw_login'])
	if request.method == "POST":
		response = Users.objects.login(request.POST)
		
		if response['status'] == True:
			print "name: ", response['user'].name
			print "id: ", response['user'].id
			request.session['name'] = response['user'].name
			request.session['id'] = response['user'].id
			return redirect('travel:travel')
		else:
			for error in response['errors']:
				messages.error(request, error)
	return redirect('/')


def logout(request):
	request.session.flush()
	messages.add_message(request, messages.SUCCESS, "You have logged out!" )
	return redirect('/')