from django.shortcuts import render
from django.http import HttpResponse
from dashboard.models import ImageList
import os



# Create your views here.



def home(request):
	context = os.listdir('surveillance/media/images')
	return render(request, "dashboard/home.html", {'images': context})
