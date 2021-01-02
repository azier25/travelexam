from django.db import models
import re
from datetime import *


class UserManager(models.Manager):
	def register(self, postData):

		USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9]+$')

		PASSWORD_REGEX = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d,!@#$%^&*+=]{8,}$')

		NAME_REGEX = re.compile(r'^[a-zA-Z0-9 ]+$')

		errors = {}

		if len(postData['username']) < 1:
			errors['username'] = 'username is required!'
		if not USERNAME_REGEX.match(postData['username']):
			errors['username-invalid'] = 'Invalid user_name!'
		check = User.objects.filter(username=postData['username'])
		if len(check) > 0:
			errors['username-inuse'] = 'User Name already in use!'

		if len(postData['password']) < 1:
			errors['password'] = 'Password is required!'
		elif not PASSWORD_REGEX.match(postData['password']):
			errors['password_valid'] = 'Password must contain at least 1 number and capitalization!'

		if len(postData['password_confirm']) < 1:
			errors['password_confirm'] = 'Confirm password is required!'
		elif postData['password_confirm'] != postData['password']:
			errors['passwords_match'] = 'Password must match Confirm password!'

		if len(postData['name']) < 2:
			errors["name"] = " name should be at least 2 characters"
		elif not NAME_REGEX.match(postData['name']):
			errors["name"] = " Name only conatains letter"

		return errors

	def login(self, postData):
		messages = []

		if len(postData['username']) < 1:
			messages.append('Username is required!')

		if len(postData['password']) < 1:
			messages.append('Password is required!')

		return messages


class TripManager(models.Manager):
	def create_trip(self, postData):
		err_message = []

		if len(postData['dest']) < 3:
			err_message.append('A trip destination must consist of at least 3 characters')
		if len(postData['plan']) < 3:
			err_message.append('A plan must be provided')
		if len(postData['start_date']) < 10:
			err_message.append("Please enter Start Date")
		elif len(postData['start_date']) == 10:
			start_date = datetime.strptime(postData['start_date'], '%Y-%m-%d')
			if start_date:
				start_date = start_date.date()
			if start_date < date.today():
				err_message.append('Start date must be today or in the future.')

		if len(postData['end_date']) < 10:
			err_message.append("Please enter End Date")
		elif len(postData['end_date']) == 10:
			end_date = datetime.strptime(postData['end_date'], '%Y-%m-%d')
			if end_date:
				end_date = end_date.date()
			if end_date < date.today():
				err_message.append('End date must be today or in the future.')

		if len(postData['end_date']) < 10 or len(postData['start_date']) < 10:
			print('error')
		else:
			if start_date > end_date:
				err_message.append('End date must be after or the same as start date.')
		return err_message


class User(models.Model):
	password = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()


class Trip(models.Model):
	user_id = models.ManyToManyField(User, related_name='user_id')
	created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.CASCADE)
	destination = models.CharField(max_length=45)
	start_date = models.DateField()
	end_date = models.DateField()
	plan = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = TripManager()

	def __repr__(self):
		return f"<User object: {self.username}>"
