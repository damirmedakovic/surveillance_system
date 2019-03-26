from django.contrib import admin
from django.urls import include, path
from . import views



app_name = "dashboard"

urlpatterns = [
	path('', views.home, name='home'),
	path('create-camera/', views.create_camera, name='create-camera'),

]
