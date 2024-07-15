from django.contrib.auth import get_user_model

class CustomAdminBackend:
    def authenticate(self, request, username=None, password=None):
        # Add your custom authentication logic here
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and user.is_superuser:
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
