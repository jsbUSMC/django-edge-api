from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'apps.profiles'
    label = 'profiles'
    verbose_name = 'User Profiles'

    def ready(self):
        #pylint: disable=W0612
        from . import signals
