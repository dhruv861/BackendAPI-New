from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Exercise)
admin.site.register(CustomUser)

admin.site.register(RecentlySelectedExercise)
admin.site.register(UserPlan)
admin.site.register(Queries)