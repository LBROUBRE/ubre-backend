from django.conf.urls import url
from ubrebackend.app.user.views import UserRegistrationView
from ubrebackend.app.user.views import UserLoginView

urlpatterns = [
    url(r'^signup', UserRegistrationView.as_view()),
    url(r'^signin', UserLoginView.as_view()),
    ]