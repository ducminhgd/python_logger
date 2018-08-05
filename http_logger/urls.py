from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from http_logger.views import daily_logger_http, mongo_logger_http

urlpatterns = [
    url(r'^http-daily-logger[/]?$', csrf_exempt(daily_logger_http.HTTPDailyLogView.as_view())),
    url(r'^http-mongo-logger[/]?$', csrf_exempt(mongo_logger_http.HTTPMongoLogView.as_view())),
]
