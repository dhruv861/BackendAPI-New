from django.urls import path
from .views import SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserProfileView, UserRegistrationView, UserPasswordResetView,GoogleSocialAuthView
from api.views import FavouritesAPIView,ExercisePlanByUser

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('google/', GoogleSocialAuthView.as_view()),
    path('exercises/favourites/',FavouritesAPIView.as_view()),
    path('exercise-plan/save/', ExercisePlanByUser.as_view())
]
