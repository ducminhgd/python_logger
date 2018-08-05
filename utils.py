# coding=utf-8
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
