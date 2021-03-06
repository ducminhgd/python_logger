# coding=utf-8

from django.utils import timezone
import datetime
import decimal
import json
import os
import time
import traceback


def format_stack_trace(exc_info):
    """
    Format exception info as string
    :param exc_info: exception info
    :return: string
    :example:

    import sys

    try:
        ...
    except:
        exc_info = sys.exc_info()
        print(format_stack_trace(exc_info))
    """
    if exc_info[0] is None:
        return ''
    lines = traceback.format_exception(*exc_info)
    return ''.join(line for line in lines)

def cleanup(day_keep_alive, file_name):
    log_dir = os.path.dirname(file_name)
    current_time = time.time()
    day_conversion_unit = 24 * 3600
    for f in os.listdir(log_dir):
        if not f.endswith('.log'):
            continue
        file_path = os.path.join(log_dir, f)
        modified_time = os.path.getctime(file_path)
        if (current_time - modified_time) // day_conversion_unit <= day_keep_alive:
            continue
        os.unlink(file_path)

class ExtendedJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            if timezone.is_aware(obj):
                obj = timezone.localtime(obj)
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)
