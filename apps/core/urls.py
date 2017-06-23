from django.conf.urls import url, include


#pylint: disable=invalid-name
urlpatterns = [
    url(r'^auth/', include('apps.authentication.urls', namespace='authentication')),
    url(r'^profiles/', include('apps.profiles.urls', namespace='profiles')),
]
