from django.utils import timezone
import datetime
import decimal
import json
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


def format_exc_info(exc_info):
    """
    Format exception info as string
    :param exc_info: exception info
    :return: string
    """
    if exc_info[0] is None:
        return 'None'
    lines = traceback.format_exception(*exc_info)
    return ''.join(line for line in lines)


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
