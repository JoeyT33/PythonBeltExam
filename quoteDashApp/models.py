from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
	def addUserValidator(self, auv):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		User.objects.filter(email = auv['email'])
		duplicateEmail = User.objects.filter(email = auv['email'])
		errors = {}
		if len(auv['fname']) == 0:
			errors['fnamereq'] = "First Name is requried!"
		elif len(auv['fname']) < 2:
			errors['fnamelen'] = "First Name must be at least 2 characters long!"

		if len(auv['lname']) == 0:
			errors['lnamereq'] = "Last Name is requried!"
		elif len(auv['lname']) < 2:
			errors['lnamelen'] = "Last Name must be at least 3 characters long!"

		if len(auv['email']) == 0:
			errors['emailreq'] = "Email is requried!"
		elif not EMAIL_REGEX.match(auv['email']):
			errors['invalidemail'] = "Invalid Email"
		elif len(duplicateEmail)>0:
			errors['dupemail'] ="This email is taken. Please use a new email and try again. Thank you!"

		if len(auv['pw']) == 0:
			errors['pwreq'] = "Password is requried!"
		elif len(auv['pw']) < 8:
			errors['pwlen'] = "Password must be at least 8 characters long!"

		if auv['pw'] != auv['cpw']:
			errors['pwMatch'] = "Passwords must match!"



		return errors

	def loginValidator(self, lgnv):
		errors = {}
		matchingEmail = User.objects.filter(email = lgnv['email'])
		if len(matchingEmail) == 0:
			errors['noemail'] = "Email not found. Please register!"

		elif not bcrypt.checkpw(lgnv['pw'].encode(), matchingEmail[0].password.encode()):
			errors['incorrectpw'] = "Passwords do not match"
		return errors
	
	def addQuoteValidator(self, aqv):
		errors ={}
		if len(aqv['afname']) == 0:
			errors['fnamereq'] = "Author first name is requried!"
		elif len(aqv['afname']) < 3:
			errors['fnamelen'] = "Author first name must be at least 3 characters long!"

		if len(aqv['alname']) == 0:
			errors['lnamereq'] = "Author last name is requried!"
		elif len(aqv['alname']) < 3:
			errors['lnamelen'] = "Author last name must be at least 3 characters long!"

		if len(aqv['quote']) < 10:
			errors['quotelen'] = "Quote must be at least 10 characters long!"
		return errors

	def editProfileValidator(self, epv):
		errors = {}
		if len(epv['fname']) == 0:
			errors['fnamereq'] = "First Name is requried!"
		elif len(epv['fname']) < 2:
			errors['fnamelen'] = "First Name must be at least 2 characters long!"

		if len(epv['lname']) == 0:
			errors['lnamereq'] = "Last Name is requried!"
		elif len(epv['lname']) < 2:
			errors['lnamelen'] = "Last Name must be at least 3 characters long!"

		if len(epv['email']) == 0:
			errors['emailreq'] = "Email is requried!"
		return errors
		

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()	

class Author(models.Model):
	firstName = models.CharField(max_length=255)
	lastName = models.CharField(max_length=255)
	quote = models.CharField(max_length=255)
	postedBy = models.ForeignKey(User, related_name="posted_by", on_delete = models.CASCADE)
	likedBy = models.ManyToManyField(User, related_name="liked_by")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

