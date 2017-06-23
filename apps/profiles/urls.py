from django.conf.urls import url

from .views import ProfileRetrieveAPIView

urlpatterns = [
    url(r'^(?P<username>\w+)/?$', ProfileRetrieveAPIView.as_view()),
]
