from django.views.generic import View
from django.http import HttpResponse

from http_logger import forms


class HTTPLoggingView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            data = request.POST.dict()
        else:
            data = request.GET.dict()
        form = forms.LogForm(data=data)
        if not form.is_valid():
            print(form.errors)
            return HttpResponse('', status=400)
        form.write_file()
        return HttpResponse('', status=201)
