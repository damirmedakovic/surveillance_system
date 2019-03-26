from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()



class AddCameraForm(forms.Form):

	name = forms.CharField(max_length=25)
	identifier = forms.CharField(max_length=25)
