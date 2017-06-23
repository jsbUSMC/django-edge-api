from __future__ import unicode_literals

import time
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.encoding import python_2_unicode_compatible

from apps.core.models import TimestampedModel


class UserManager(BaseUserManager):
    """
    Django requires any custom user class to define its own `UserManager` class. This class
    needs to inherit from BaseUserManager, from the django.contrib.auth.models package.

    The only required overrides are for the create_user() and create_superuser() methods.
    We will override these to implement the functionality we need using the fiels defined
    on our custom model.
    """
    def create_user(self, email, password=None, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


@python_2_unicode_compatible
class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    """
    The `User` class makes use of the `AbstractBaseUser` class provided by Django to
    customize the User to our own needs without relying on the built-in `User` model.
    Specifically, we want to add timestamps for creation, by extending the abstract
    class `TimestampedModel`, remove the `first_name` and `last_name` fields in favor
    of a unified `name` field, and require email as a unique user identifier, instead
    of having a redundant username and email specifier per user.

    Here we also specify that our model is implement the methods `token()` and
    `_generate_jwt_token()`. This way, we can create, access and verify the JWT
    that is generated upon login.
    """
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    name = models.CharField(_('name'), max_length=255)

    #pylint: disable=bad-continuation
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['name', 'email']

    def __str__(self):
        return '{name} <{email}>'.format(
            name=self.name,
            email=self.email,
        )

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""

        send_mail(subject, message, from_email, [self.email], **kwargs)

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
        exactdatetime = datetime.now() + timedelta(days=60)

        # Quick Windows 7 hack: the 'exp' key trips fatal exception for invalid formatted
        # string. Replace the commented out line on mac OS
        token = jwt.encode({
            'id': self.pk,
            # 'exp': int(exactdatetime.strftime('%s'))
            'exp': str(time.mktime(exactdatetime.timetuple()))[:-2]
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
