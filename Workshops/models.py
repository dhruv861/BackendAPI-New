from django.db import models

# Create your models here.

class Workshop(models.Model):
    room_id = models.CharField(max_length=200)
    name= models.CharField(max_length=100)
    description = models.TextField()
    enabled = models.BooleanField(default=False)
    image = models.URLField()

    def __str__(self):
        return self.name
