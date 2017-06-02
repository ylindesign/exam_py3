from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse

from django.contrib import messages
from .models import Travel
from ..login.models import Users

def travel(request):
	if not 'name' in request.session:
		messages.add_message(request, messages.ERROR, "Can't skip login!")
		return redirect('/')

	user = Users.objects.get(id=request.session['id'])

	context = {
		'my_trips': Travel.objects.filter(join=user),
		# 'joined_trips': Travel.objects.filter(join=),
		'other_trips': Travel.objects.exclude(join=user),
		# 'now': datetime.date.today()
		# 'all': Task.objects.all(),
	}
	return render(request, 'travel/travel.html', context)

def add(request):

	return render(request, 'travel/add.html')

def new(request, id):
	if request.method == "POST":
		id = request.session['id']
		trip = {
			'dest': request.POST['dest'],
			'start': request.POST['start'],
			'end': request.POST['end'],
			'plan': request.POST['plan'],
			'person': id,
		}

	response = Travel.objects.new(trip)
	# print "Status: ", response['status']
	if response['status'] == False:
		for error in response['errors']:
			messages.add_message(request, messages.ERROR, error)
		return redirect("travel:add")
	else:
		messages.add_message(request, messages.SUCCESS, "Trip Added!" )
	return redirect('travel:travel')


def dest(request, id):
	place = Travel.objects.get(id=id)
	creator = place.created_by.id
	print "creator: ", creator
	print "place name: ", place.dest
	context = {
		'place': place,
		'joined': place.join.exclude(id=creator)
	}
	print "joined: ", context['joined']
	return render(request, 'travel/dest.html', context)

def join(request, trip_id):
	if request.method == "POST":
		# id = request.session['id']
		trip = {
			'trip': trip_id,
			'person': request.session['id'],
		}

		Travel.objects.join(trip)
	messages.add_message(request, messages.SUCCESS, "Trip Joined!" )
	return redirect('travel:travel')

def delete(request, trip_id):
	Travel.objects.get(id=trip_id).delete()
	return redirect('travel:travel')



