from django.db import models
#from django.conf import settings
#from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model

# Create your models here.


def media_directory_path(instance, filename):
    return "./map_grids/{0}/{1}_{2}.png".format(instance.zoom_layer.zoom_layer, instance.x_coord, instance.y_coord)


# class OverwriteStorage(FileSystemStorage):
#
#     def get_available_name(self, name, max_length=None):
#         # If the filename already exists, remove it as if it was a true file system
#         if self.exists(name):
#             self.delete(name)
#         return name


class Grid(models.Model):
    grid_id = models.IntegerField(primary_key=True)
    x_coord = models.IntegerField(null=False)
    y_coord = models.IntegerField(null=False)
    update_timestamp = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.grid_id} - ({self.x_coord} , {self.y_coord})"


class CharacterLocation(models.Model):
    name = models.TextField()
    gob_id = models.IntegerField()
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
    time_added = models.DateTimeField(default=timezone.now)

    class Meta:
        models.Index(fields=['-time_added'])

    def __str__(self):
        return f"{self.name} - ({self.x_coord} , {self.y_coord} - {self.time_added})"


class MarkerData(models.Model):
    grid_id = models.IntegerField()
    name = models.TextField()
    image = models.TextField()
    x_coord = models.IntegerField(null=False)
    y_coord = models.IntegerField(null=False)
    hidden = models.BooleanField(default=False)
    #update_timestamp = models.DateField(null=True)

    def __str__(self):
        return f"{self.name} - ({self.x_coord} , {self.y_coord})"


class LostMarkerData(models.Model):
    grid_id = models.IntegerField()
    name = models.TextField()
    image = models.TextField()
    x_coord = models.IntegerField(null=False)
    y_coord = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.name} - ({self.x_coord} , {self.y_coord})"


class GeneratedToken(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    token = models.TextField(default=get_random_string)

    def __str__(self):
        return f"{self.owner} - {self.token})"

