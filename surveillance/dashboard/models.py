from django.db import models

# Create your models here.


class ImageList(models.Model):
    image = models.ImageField(upload_to="images", blank=True)

    #def __str__(self):
        #return self.title