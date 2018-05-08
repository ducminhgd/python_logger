# coding: utf-8

import datetime
import os
from django import forms
from django.utils import timezone, six


class DailyFileManager(object):

    def __init__(self):
        self.open_files = {}
        self.current_dates = {}

    def is_open(self, file_name):
        current_date = timezone.now().date()

        if file_name in self.current_dates and self.current_dates[file_name] != current_date:
            is_diff_date = True
        else:
            is_diff_date = False

        if is_diff_date:
            # Archive file
            old_current_date = self.current_dates[file_name]
            archive_file_name = '%s.%s' % (file_name, old_current_date)

            opened_file = self.open_files.get(file_name, None)
            if opened_file:
                opened_file.close()
            if os.path.exists(archive_file_name):
                with open(archive_file_name, 'a') as fp:
                    temp = open(file_name, 'r')
                    fp.write(temp.read())
                    temp.close()
            else:
                os.rename(file_name, archive_file_name)

            self.current_dates[file_name] = current_date
            for key in self.open_files:
                self.open_files[key].close()
                self.open_files[key] = open('%s' % key, 'a')
        if file_name in self.open_files:
            return True
        return False

    def open(self, file_name):
        self.current_dates[file_name] = timezone.now().date()
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

    def write_file(self):
        created = self.cleaned_data['created']

        levelname = self.cleaned_data["levelname"]
        process = self.cleaned_data['process']
        thread = self.cleaned_data['thread']

        filename = self.cleaned_data['filename']
        lineno = self.cleaned_data["lineno"]
        module = self.cleaned_data['module']

        funcName = self.cleaned_data["funcName"]
        msg = self.cleaned_data['msg']

        logPath = self.cleaned_data["logPath"]
        time = datetime.datetime.fromtimestamp(float(created)).strftime('%Y-%m-%d %H:%M:%S')

        data = "%s | %s | %s:%s | %s:%s | %s.%s | %s \n" % (
            time, levelname, process, thread, filename, lineno, module, funcName, msg
        )

        if not daily_file_manager.is_open(logPath):
            daily_file_manager.open(logPath)

        if six.PY2:
            data = data.encode('UTF-8')

        daily_file_manager.write(logPath, data)
