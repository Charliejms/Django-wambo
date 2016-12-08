import datetime
import re  # regular expresions
import math

from django.utils.html import strip_tags


def count_words(html_string):
    """
    Contar palabras escitas
    :param html_string:
    :return:
    """
    words_string = strip_tags(html_string)
    count = len(re.findall(r'\w+', words_string))
    return count


def get_read_time(in_string):
    count = count_words(in_string)
    read_time_min = math.ceil(count/200.0)  # velocidad de lectora  = 200
    read_time = str(datetime.timedelta(minutes=read_time_min))
    return read_time
