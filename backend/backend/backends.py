from django.contrib.auth.backends import BaseBackend
from web.models import Registros


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Registros.objects.get(usuario=username)
            if user.check_password(password):
                return user
        except Registros.DoesNotExist:
            return None
