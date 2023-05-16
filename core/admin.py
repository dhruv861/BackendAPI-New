from django.contrib import admin
from .models import Exercise,CustomUser,Gym,Favourite,RecentlySelectedExercise
# Register your models here.

admin.site.register(Exercise)
admin.site.register(CustomUser)
admin.site.register(Gym)
admin.site.register(Favourite)
admin.site.register(RecentlySelectedExercise)