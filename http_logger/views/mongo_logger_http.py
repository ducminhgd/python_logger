from django.views.generic import View
from django.http import HttpResponse

from http_logger import forms


class HTTPMongoLogView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            data = request.POST.dict()
        else:
            data = request.GET.dict()
        form = forms.DailyLogForm(data=data)

        if not form.is_valid():
            return HttpResponse('', status=400)
        form.store_db()
        return HttpResponse('', status=201)
