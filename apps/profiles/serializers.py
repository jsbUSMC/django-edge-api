from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from phonenumber_field.phonenumber import to_python

from .models import Profile


class PhoneNumberField(serializers.CharField):
    default_error_messages = {
        'invalid': _('Enter a valid phone number.'),
    }

    def to_internal_value(self, data):
        phone_number = to_python(data)
        if phone_number and not phone_number.is_valid():
            raise ValidationError(self.error_messages['invalid'])
        return phone_number


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    name = serializers.CharField(source='user.name')
    slug = serializers.UUIDField()
    bio = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    job_title = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    primary_phone = PhoneNumberField(allow_blank=True, allow_null=True, required=False)
    secondary_phone = PhoneNumberField(allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = Profile
        fields = (
            'email',
            'bio',
            'name',
            'job_title',
            'slug',
            'primary_phone',
            'secondary_phone',
        )
        read_only_fields = ('email', 'name', 'slug',)
