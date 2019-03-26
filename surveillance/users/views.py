from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from dashboard import urls

#from shopping_list import views

# Create your views here.



def home(request):
	return render(request, "users/home.html")

def register(request):

	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			login(request, user)
			messages.success(request, f'Registered {username} and logged in successfully!')
			return redirect("dashboard:home")
		else:
			for msg in form.errors:
				messages.error(request, f"{form.errors[msg]}")
				return redirect("users:register")

	form = UserCreationForm()
	return render(request, "users/register.html", context={"form": form})


def registered(request):
	return redirect('users:login')


def logout_request(request):
	logout(request)
	test = redirect('users:login')
	messages.success(request, 'Logged out successfully!')

	return test


def login_request(request):

	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(username=username, password=password)
			messages.success(request, f'Succesfully logged in as {username}!')
			if user is not None:
				login(request, user)
				return redirect("dashboard:home")
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")

		render(request, "users/login.html", {"form": form})

	form = AuthenticationForm()

	return render(request, "users/login.html", {"form": form})