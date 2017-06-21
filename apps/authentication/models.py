from authtools.models import User
import jwt
from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Analyst(User):
    """
    The `Analyst` class makes use of the `User` class provided by the django-authtools
    package. This concrete class implements abstract class `AbstractNamedUser`, which
    itself implements the abstract class `AbstractEmailUser`, so that our users don't
    have to register a separate first/last name and uses email as default username.

    Here we specify that our model is simply a proxy on the authtools' `User` class so
    that we can implement the methods `token()` and `_generate_jwt_token()`. Because we
    only add methods/functionality to the inherited `User` model, we don't need Django
    ORM to create separate db tables for this class.
    """
    class Meta:
        proxy = True

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
