from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import *


def index(request):
	return render(request, 'index.html')


def addUser(request):
	errorsfromauv = User.objects.addUserValidator(request.POST)

	if len(errorsfromauv)>0:
		for key, value in errorsfromauv.items():
			messages.error(request, value)
		return redirect("/")
	
	encryptPw = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()

	newuser = User.objects.create(first_name = request.POST['fname'], last_name = request.POST['lname'], email = request.POST['email'], password = encryptPw)

	request.session['loggedInUserId'] = newuser.id

	return redirect("/quotes")

def quotes(request):
	if 'loggedInUserId' not in request.session:
		messages.error(request, "You must be logged in to move on")
		return redirect("/")

	context = {
		'welcomeUser': User.objects.get(id=request.session['loggedInUserId']),
		'allquotes': Author.objects.all(),
		'allusers': User.objects.all()
	}
	return render(request, 'welcome.html', context)

def logout(request):
	request.session.clear()
	return redirect("/")

def login(request):
	errorsfromlgnv = User.objects.loginValidator(request.POST)

	if len(errorsfromlgnv)>0:
		for key, value in errorsfromlgnv.items():
			messages.error(request, value)
		return redirect("/")
	matchingemail = User.objects.filter(email = request.POST['email'])
	request.session['loggedInUserId'] = matchingemail[0].id
	return redirect("/quotes")

def addQuote(request):
	errorsfromaqv = User.objects.addQuoteValidator(request.POST)

	if len(errorsfromaqv)>0:
		for key, value in errorsfromaqv.items():
			messages.error(request, value)
		return redirect("/quotes")

	firstLike = Author.objects.create(firstName = request.POST['afname'], lastName = request.POST['alname'], quote = request.POST['quote'], postedBy = User.objects.get(id=request.session['loggedInUserId']))

	User.objects.get(id=request.session['loggedInUserId']).liked_by.add(firstLike)

	return redirect("/quotes")

def viewQuotes(request, userid):
	context = {
		'allquotes': User.objects.get(id=userid)
	}
	return render(request, 'quotelist.html', context)

def viewAccount(request, userid):
	context = {
		'welcomeUser': User.objects.get(id=request.session['loggedInUserId']),
			}

	return render(request, 'profile.html', context)

def editProfile(request, userid):
	errorsfromepv = User.objects.editProfileValidator(request.POST)

	if len(errorsfromepv)>0:
		for key, value in errorsfromepv.items():
			messages.error(request, value)
		return redirect(f"/myaccount/{userid}")

	editacct = User.objects.get(id=userid)
	editacct.first_name = request.POST['fname'] 
	editacct.last_name = request.POST['lname']
	editacct.email = request.POST['email']
	editacct.save()
	return redirect("/quotes")

def likeThis(request ,quoteid):
	this_user = User.objects.get(id=request.session['loggedInUserId'])
	this_quote = Author.objects.get(id=quoteid)
	this_quote.likedBy.add(this_user)
	return redirect("/quotes")