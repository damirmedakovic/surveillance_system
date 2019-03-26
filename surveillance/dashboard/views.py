from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
from .forms import AddCameraForm
from .models import SecurityCamera, ValidIdentifier
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages



# Create your views here.


def home(request):

	form = AddCameraForm
	owned_cameras = SecurityCamera.objects.filter(owners=request.user)
	owned_cameras_id = []
	for camera in owned_cameras:
		owned_cameras_id.append(camera.identifier)

	print("HEEEEY", owned_cameras_id)

	context = {'images': os.listdir('surveillance/media/images'),
			   'camera_form': form,
			   'owned_camera_id': owned_cameras_id
				}
	return render(request, "dashboard/home.html", context)


@login_required(login_url='')
@require_POST
def create_camera(request):

	valid_identifiers = ValidIdentifier.objects.all()
	identifiers = []
	for idf in valid_identifiers:
		identifiers.append(idf.identifier)

	if request.method == "POST":
		owner = request.user
		camera_form = AddCameraForm(request.POST)
		if camera_form.is_valid(): 
			camera_name = camera_form.cleaned_data['name']
			camera_identifier = camera_form.cleaned_data['identifier']
			if camera_identifier in identifiers:
				new_security_camera = SecurityCamera(name=camera_name, identifier=camera_identifier)
				new_security_camera.save()
				new_security_camera.owners.add(owner)
				messages.success(request, f'Successfully registered camera with name *{camera_name}* and identifier *{camera_identifier}*! You can now monitor this camera.')
				return redirect("dashboard:home")
			else:
				messages.error(request, "The provided identifier is not registered with any camera. Make sure it's typed correctly.")
				return redirect("dashboard:home")
	else:
		messages.error(request, "The provided identifier is not registered with any camera. Make sure it's typed correctly.")
		return redirect("dashboard:home")

