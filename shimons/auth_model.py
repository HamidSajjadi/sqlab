from django.conf import settings
from django.contrib.auth.hashers import check_password
from shimons.models import UserProfile


class AuthBackend:
    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, email=None, password=None):
        try:

            # Try to find a user matching your username
            user = UserProfile.objects.get(email=email)
            print(email, password)
            print(user)
            #  Check the password is the reverse of the username
            if check_password(password, user.password):
                # Yes? return the Django user object
                return user
            else:
                # No? return None - triggers default login failed
                return None
        except UserProfile.DoesNotExist:
            # No user was found, return None - triggers default login failed
            return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return None
