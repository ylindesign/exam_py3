from __future__ import unicode_literals

from django.db import models
from ..login.models import Users

from datetime import date
import datetime
from django.db.models import Count

class TravelManager(models.Manager):
	def new(self, trip):
		response = {}
		errors = []
		print "Today is: ", date.today()
		print "Start is: ", trip['start']
		print "End is: ", trip['end']
		if len(trip['dest']) < 1 or len(trip['start']) < 1 or len(trip['end']) < 1 or len(trip['plan']) < 1:
			errors.append('Nothing can be blank')
			response['status'] = False
			response['errors'] = errors
			return response
		if len(trip['start']) > 1 or len(trip['end']) > 1:
			if trip['start'] > trip['end']: 
				errors.append('Cant end trips before they start')
				response['status'] = False
				response['errors'] = errors
				return response
			elif trip['start'] == trip['end']:
				errors.append('Dont go and leave on the same day!')
				response['status'] = False
				response['errors'] = errors
				return response
			elif trip['start'] > 0 or trip['end'] > 0:
				if str(trip['start']) < str(date.today()) or str(trip['end']) < str(date.today()):
					errors.append('Cant make a trip in the past')
					response['status'] = False
					response['errors'] = errors
					return response
			else:
				print "Im trying to add it here!"
				person = Users.objects.get(id=trip['person'])
				trip = Travel.objects.create(dest=trip['dest'], start=trip['start'], end=trip['end'], plan=trip['plan'], created_by=person)
				trip.join.add(person)
				trip.save()
				response['status'] = True
		return response

	def join(self, trip):
		person = Users.objects.get(id=trip['person'])
		Travel.objects.get(id=trip['trip']).join.add(person)
		# joining.joined.add(person)
		return


class Travel( models.Model ):
    dest = models.CharField( max_length = 255 )
    created_by = models.ForeignKey( Users, related_name = "created_by" )
    start = models.DateField()
    end = models.DateField()
    plan = models.CharField( max_length = 255 )
    join = models.ManyToManyField( Users, related_name = "joined" )
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )

    objects = TravelManager()