from django.views.generic import View
from django.http import HttpResponse
import json
from http_logger.forms import mongo_log_form


class HTTPMongoLogView(View):
    def dispatch(self, request, *args, **kwargs):
        data = json.loads(json.loads(request.body.decode('utf-8')))
        form = mongo_log_form.MongoLogJson(data=data)

        if not form.is_valid():
            return HttpResponse('', status=400)
        form.store_db()
        return HttpResponse('', status=201)
