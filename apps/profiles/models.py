from __future__ import unicode_literals

import uuid

from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from apps.core.models import TimestampedModel


class BaseProfile(TimestampedModel):
    # As mentioned, there is an inherent relationship between the Profile and
    # User models. By creating a one-to-one relationship between the two, we
    # are formalizing this relationship. Every user will have one -- and only
    # one -- related Profile model.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False)
    job_title = models.CharField(max_length=75, blank=True, null=True)
    primary_phone = PhoneNumberField(blank=True, null=True)
    secondary_phone = PhoneNumberField(blank=True, null=True)

    # Each user profile will have a field where they can tell other users
    # something about themselves. This field will be empty when the user
    # creates their account, so we specify `blank=True`.
    bio = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

@python_2_unicode_compatible
class Profile(BaseProfile):
    def __str__(self):
        return "{}'s profile". format(self.user)
