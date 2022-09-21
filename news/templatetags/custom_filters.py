from atexit import register
from django import template
import re
import os

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    if isinstance(value, str) and isinstance(arg, int):
        return str(value) * arg
    else:
        raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}')

def get_badwords_list():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file_name = os.path.join(base_dir, 'taboo.txt')
    with open(file_name, 'r') as f:
        taboo_list = [line.strip() for line in f.readlines()]
    return taboo_list

@register.filter(name='censor')
def replace_badwords(input_text, replacement_char = '*'):
    badwords_list = get_badwords_list()
    #badwords_list = ['волк', 'мир', 'раб', 'linux', 'мах','поп', 'королев']
    res = input_text
    for word in badwords_list:
        # word = r'\b%s\b' % word
        # print(word)
        regex = re.compile(word, re.IGNORECASE)
        # res = regex.sub('*' * (len(word) - 4), res)
        res = regex.sub(replacement_char * len(word), res)
    return res