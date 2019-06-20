from accounts.models import User, Token


class PasswordlessAuthenticationBackend(object):
    # https://stackoverflow.com/questions/51870788/django-custom-authentication-back-end-doesnt-work/51885328
    # custom authentication backend class now expects parameter request in method authenticate after 2.1
    def authenticate(self, request, uid):
        print("PPPP:", uid)

        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
