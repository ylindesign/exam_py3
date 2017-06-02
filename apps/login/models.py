from __future__ import unicode_literals

from django.db import models

import re, md5

PW_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')


class UsersManager(models.Manager):
	def regis(self, person):
		response = {}
		errors = []
		if len(person['name']) < 3 or len(person['username']) < 3:
			errors.append('Name and username needs to be at least 3 characters')
		if len(person['password']) < 8:
			errors.append('Password must be at least 8 characters')
		if Users.objects.filter(username = person['username']):
			errors.append('Username is taken!')		
		if not (person['password']) == (person['conf_pw']):
			errors.append('Passwords must match!')
		if errors:
			response['status'] = False
			response['errors'] = errors
		else:
			hashed_pw = md5.new(person['password']).hexdigest()
			print "hashed_pw at regis", hashed_pw
			response['status'] = True
			response['person'] = self.create(name=person['name'], username=person['username'], password=hashed_pw)
		return response

	def login(self, postData): #Coming in as request.POST
		response = {}
		errors = []
		if len(postData['username_login']) < 1 or len(postData['pw_login']) < 1:
			errors.append('Username and/or Password cant be left blank')	
			response['status'] = False
			response['errors'] = errors
			return response	
		else:
		# try:
			user = self.get(username=postData['username_login'])
			print user
			login_hash = md5.new(postData['pw_login']).hexdigest()
			print "login hash:", login_hash
			print "user password:", user.password
			print "user username:", user.username

			if user.password == login_hash:
				print "passwords match!"
				response['status'] = True
				response['user'] = user
				return response
			else:
				response ['status'] = False
				return response
		# except:
		# 	print "failed!!!"

class Users( models.Model ):
    name = models.CharField( max_length = 255 )
    username = models.CharField( max_length = 255 )
    password = models.CharField( max_length = 40 )
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )

    objects = UsersManager()