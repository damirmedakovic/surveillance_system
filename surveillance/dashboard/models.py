from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.



User = get_user_model()


class SecurityCamera(models.Model):
    name = models.CharField(max_length=25, default="default name")
    owners = models.ManyToManyField(User, default=1, related_name='owners')
    identifier = models.CharField(max_length=25, default="default")

    def __str__(self):
        return self.name


class ValidIdentifier(models.Model):
	identifier = models.CharField(max_length=25)
