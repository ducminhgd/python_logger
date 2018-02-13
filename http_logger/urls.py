from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt


from http_logger import views

urlpatterns = [
    url(r'^http-daily-logger[/]?$', csrf_exempt(views.HTTPDailyLogView.as_view())),
]
