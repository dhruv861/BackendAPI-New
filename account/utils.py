from django.core.mail import EmailMessage
import os
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
# from.views import get_tokens_for_user
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import CustomUser


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request())

            if 'accounts.google.com' in idinfo['iss']:
                return idinfo

        except:
            return "The token is either invalid or has expired"


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get('EMAIL_FROM'),
            to=[data['to_email']]
        )
        email.send()
    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    @staticmethod
    def register_social_user( provider, user_id, email, name):
        filtered_user_by_email = CustomUser.objects.filter(email=email)

        if filtered_user_by_email.exists():

            # if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=os.environ.get('SOCIAL_SECRET'))
            print(registered_user)
            return {
                # 'username': registered_user.username,
                'email': registered_user.email,
                'tokens': Util.get_tokens_for_user(registered_user)}

            # else:
            #     raise AuthenticationFailed(
            #         detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        else:
            user = {
                'name': name, 'email': email,
                'password': os.environ.get('SOCIAL_SECRET')}
            user = CustomUser.objects.create_user(**user)
            user.is_verified = True
            user.auth_provider = provider
            user.save()

            new_user = authenticate(
                email=email, password=os.environ.get('SOCIAL_SECRET'))
            return {
                'email': new_user.email,
                'username': new_user.username,
                'tokens': Util.get_tokens_for_user(new_user)
            }
