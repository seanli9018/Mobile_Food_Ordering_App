import jwt
from time import time
from mtserver import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header, exceptions
from jwt.exceptions import ExpiredSignatureError
from django.contrib.auth import get_user_model
User = get_user_model()


def generate_jwt(user, exp_days=7):
    expiration_timestamp = int(time() + (exp_days * 24 * 60 * 60))
    return jwt.encode({'userid': user.pk, 'exp': expiration_timestamp}, settings.SECRET_KEY).decode('utf-8')


class JWTAuthentication(BaseAuthentication):
    """
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "JWT ".  For example:

        Authorization: JWT 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'JWT'

    def authenticate(self, request):
        # auth here is a bytes string type (NOT string)
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            jwt_token = auth[1]
            jwt_info = jwt.decode(jwt_token, settings.SECRET_KEY)
            userid = jwt_info.get('userid')
            try:
                user = User.objects.get(pk=userid)
                return user, jwt_token
            except ValueError:
                msg = 'User dose not exist!'
                raise exceptions.AuthenticationFailed(msg)
        except ExpiredSignatureError:
            msg = 'Token expired!'
            raise exceptions.AuthenticationFailed(msg)
