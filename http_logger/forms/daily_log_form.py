# coding: utf-8

import datetime
import os
from django import forms
from django.utils import timezone, six
from common.utils import cleanup


class DailyFileManager(object):

    def __init__(self):
        self.open_files = {}
        self.current_date = timezone.now().date()

    def is_open(self, file_name, day):
        if timezone.now().date() != self.current_date:
            old_current_date = self.current_date
            self.current_date = timezone.now().date()
            for key in self.open_files:
                name, ext = os.path.splitext(key)
                archive_file_name = '%s.%s%s' % (name, old_current_date, ext)

                opened_file = self.open_files.get(key, None)
                if opened_file:
                    opened_file.close()
                if os.path.exists(archive_file_name):
                    with open(archive_file_name, 'a') as fp:
                        temp = open(key, 'r')
                        fp.write(temp.read())
                        temp.close()
                else:
                    os.rename(key, archive_file_name)

                self.open_files[key] = open('%s' % key, 'a')
            # clean up
            if day is not None:
                cleanup(day, file_name)
        if file_name in self.open_files:
            return True
        return False

    def open(self, file_name):
        self.open_files[file_name] = open('%s' % file_name, 'a')

    def write(self, file_name, data):
        self.open_files[file_name].write(data)
        self.open_files[file_name].flush()


daily_file_manager = DailyFileManager()


class DailyLogForm(forms.Form):
    name = forms.CharField()
    created = forms.CharField()
    levelname = forms.CharField()
    process = forms.CharField()
    thread = forms.CharField()
    filename = forms.CharField()
    lineno = forms.CharField()
    module = forms.CharField()
    funcName = forms.CharField()
    msg = forms.CharField()
    logPath = forms.CharField()
    day = forms.IntegerField(required=False)

    def write_file(self):
        msg = self.cleaned_data['msg'] + '\n'
        logPath = self.cleaned_data["logPath"]
        day = self.cleaned_data['day']
        if not daily_file_manager.is_open(logPath, day):
            daily_file_manager.open(logPath)

        if six.PY2:
            msg = msg.encode('UTF-8')

        daily_file_manager.write(logPath, msg)
