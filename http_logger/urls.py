from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from logging import handlers

from http_logger import views

urlpatterns = [
    url(r'^http-logger[/]?$', csrf_exempt(views.HTTPLoggingView.as_view())),
]
