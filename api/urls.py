# from api.urls import *
from django.urls import path,include
from .views import *
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register(r'exercises/', exercises,basename=)

urlpatterns = [
    path('index/', index),
    path('exercises/', AllExerciseAPIView.as_view()),
    path('exercises/bodyparts/',BodyPartsAPIView.as_view()),
    path('exercises/bodyparts/<bodypart>', FilterBodyPartAPIView.as_view()),
    path('exercises/filter/', FilterTarget.as_view()),
    path('exercises/<int:id>/',ExerciseAPIView.as_view()),
    path('favourites/',FavouritesAPIView.as_view()),
    path('workshops/rooms/', AllRooms.as_view()),
    path('workshops/room-code/<role>/<roomId>',GetRoomCode.as_view()),
    path('exercise-plan/generate/', ExercisePlanGeneratorAPIView.as_view(), name='exercise-plan-generate'),

    # path('favourites/remove/',remove_from_fav)
]

# urlpatterns += router.urls