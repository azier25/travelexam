from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def home(request):
	return render(request, "index.html")


def register(request):
	errors = User.objects.register(request.POST)
	if len(errors) > 0:
		for key, error in errors.items():
			messages.error(request, error)
		return redirect("/")
	else:
		pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
		user = User.objects.create(password=pw_hash, name=request.POST['name'], username=request.POST['username'])
		request.session['user_id'] = user.id
		request.session['name'] = user.name
		messages.success(request, "Registered successfully :)")
		return redirect("/dashboard")


def login(request):
	errors = User.objects.login(request.POST)
	if errors:
		for error in errors:
			messages.error(request, error)
		return redirect("/")
	else:
		user = User.objects.filter(username=request.POST['username'])
		if len(user) < 1:
			messages.error(request, "No User for that username")
			return redirect("/")

		if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
			request.session['user_id'] = user[0].id
			request.session['name'] = user[0].name
			return redirect("/dashboard")
		else:
			messages.error(request, "Incorrect Password!")
			return redirect("/")


def logout(request):
	request.session.clear()
	messages.success(request, "Log out successful!")
	return redirect("/")


def dashboard(request):
	if 'user_id' not in request.session:
		messages.error(request, "Permission Denied")
		return redirect("/")
	context = {
		"user_id": request.session['user_id'],
		"name": request.session['name'],
		"trips": Trip.objects.all().order_by('-created_at'),
		"this_user": User.objects.get(id=request.session['user_id'])
	}
	print(f"LOG - Rendering success page")
	return render(request, "dashboard.html", context)


def new_trip(request):
	return render(request, 'create_trip.html')


def create_trip(request):
	if 'user_id' not in request.session:
		messages.error(request, "Permission Denied")
		return redirect("/")
	errors = Trip.objects.create_trip(request.POST)
	if errors:
		for error in errors:
			messages.error(request, error)
		return redirect("/new_trip")
	user = User.objects.get(id=request.session['user_id'])
	new_trip = Trip.objects.create(created_by=user, destination=request.POST['dest'],
	                               start_date=request.POST['start_date'], end_date=request.POST['end_date'],
	                               plan=request.POST['plan'])
	new_trip.user_id.add(user.id)
	messages.success(request, "Trip successfully create :)")
	return redirect('/dashboard')


def edit_trip(request, id):
	if 'user_id' not in request.session:
		messages.error(request, "Permission Denied")
		return redirect("/")
	if request.POST:
		errors = Trip.objects.create_trip(request.POST)
		if errors:
			for error in errors:
				messages.error(request, error)
			return redirect(f'/edit/{id}')
		else:
			trip = Trip.objects.get(id=id)
			trip.destination = request.POST['dest']
			trip.start_date = request.POST['start_date']
			trip.end_date = request.POST['end_date']
			trip.plan = request.POST['plan']
			trip.save()
			return redirect('/dashboard')
	else:
		context = {
			'trip': Trip.objects.get(id=id)
		}
		return render(request, 'edit_trip.html', context)


def remove(request, id):
	if "user_id" not in request.session:
		return redirect('/')
	else:
		trip = Trip.objects.get(id=id)

		trip.delete()

		return redirect('/dashboard')


def show_trip(request, id):
	if "user_id" not in request.session:
		return redirect('/')
	else:
		context = {
			"user_id": request.session['user_id'],
			'trip': Trip.objects.get(id=id),
			"trips": Trip.objects.all().order_by('-created_at')

		}
		return render(request, "show_trip.html", context)


def join_trip(request, id):
	if "user_id" not in request.session:
		return redirect('/')
	else:
		user = User.objects.get(id=request.session['user_id'])
		trip = Trip.objects.get(id=id)
		trip.user_id.add(user)
		return redirect('/dashboard')


def cancel_trip(request, id):
	trip = Trip.objects.get(id=id)
	user = User.objects.get(id=request.session['user_id'])
	trip.user_id.remove(user)
	trip.save()
	return redirect('/dashboard')