from django.conf.urls import url
from ubrebackend.app.profile.views import UserProfileView

urlpatterns = [
    url(r'^profile', UserProfileView.as_view()),
    ]