from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
from .forms import AddCameraForm
from .models import SecurityCamera, ValidIdentifier
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def update_folders(request):

	#All cameras registered to this user by id. 
	owned_cameras = SecurityCamera.objects.filter(owners=request.user)
	owned_cameras_id = []

	for camera in owned_cameras:
		owned_cameras_id.append(camera.identifier)
	owned_cameras_id = set(owned_cameras_id)

	existing_folders = os.listdir('surveillance/media/')
	existing_folders.remove('client_script.py')

	#Check if this user just registered a camera that does not have a image folder yet. 
	#If folder does not exist, create it using the unique identifier that only the user has. 
	for fld in owned_cameras_id:
		if fld not in existing_folders:
			relative_path = f'surveillance/media/{fld}'
			path = os.path.join(BASE_DIR, relative_path)
			os.mkdir(path)


def home(request):

	update_folders(request)

	form = AddCameraForm()

	#Collect all registered cameras of this user. This gets sent to the template as context.
	owned_cameras = SecurityCamera.objects.filter(owners=request.user)
	owned_cameras_id = []

	for camera in owned_cameras:
		owned_cameras_id.append(camera.identifier)
	owned_cameras_id = set(owned_cameras_id)

	cameras_dictionary = {}
	for cam in owned_cameras_id:
		cameras_dictionary[f'{cam}'] = os.listdir(f'surveillance/media/{cam}')

	context = {'cameras_dictionary': cameras_dictionary,
			   'camera_form': form
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

