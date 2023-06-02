from django.urls import path
from .views import *
from api.views import FavouritesAPIView,PlanByUser

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('google/', GoogleSocialAuthView.as_view()),
    path('exercises/favourites/',FavouritesAPIView.as_view()),
    path('exercise-plan/save/', PlanByUser.as_view()),
    path('profile/update/',UpdateProfileView.as_view())
]
