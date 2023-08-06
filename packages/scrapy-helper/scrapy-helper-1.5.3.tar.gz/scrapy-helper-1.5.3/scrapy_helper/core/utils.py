import json
import re

import lxml.html
import lxml.html.clean


def str2list(x, transformer=None):
    """
    convert to list
    :param transformer:
    :param x:
    :return:
    """
    if x is None or isinstance(x, list):
        return x
    try:
        data = json.loads(x)
        if not transformer:
            def transformer(t): return t
        data = list(map(lambda y: transformer(y), data))
        return data
    except:
        return []


def str2dict(v):
    """
    convert str to dict data
    :param v:
    :return:
    """
    try:
        return json.loads(v)
    except:
        return {}


def str2body(v):
    """
    convert str to json data or keep original string
    :param v:
    :return:
    """
    try:
        return json.loads(v)
    except:
        return v


def inner_trim(value):
    if isinstance(value, str):
        # remove tab and white space
        value = re.sub(re.compile(r'[\s\t]+'), ' ', value)
        value = ''.join(value.splitlines())
        return value.strip()
    return ''


def clean_html(node):
    # cleaner = lxml.html.clean.Cleaner()
    # cleaner.javascript = True
    # cleaner.style = True
    # cleaner.allow_tags = [
    #     'a', 'span', 'p', 'br', 'strong', 'b',
    #     'em', 'i', 'tt', 'code', 'pre', 'blockquote', 'img', 'h1',
    #     'h2', 'h3', 'h4', 'h5', 'h6',
    #     'ul', 'ol', 'li', 'dl', 'dt', 'dd']
    # cleaner.remove_unknown_tags = False
    cleaner = lxml.html.clean.Cleaner()
    cleaner.scripts = True
    cleaner.javascript = True
    cleaner.style = True
    return cleaner.clean_html(node)


def convert_to_html(element):
    if not element:
        return ''

    if isinstance(element, str):
        element = lxml.html.fromstring(element)

    clean_data = clean_html(element)
    data = lxml.html.tostring(clean_data, encoding="utf8", pretty_print=True, method='html').decode("utf-8")
    return data


def convert_to_text(element):
    if not element:
        return ''

    if isinstance(element, str):
        element = lxml.html.fromstring(element)

    text = lxml.html.tostring(element, encoding="utf8", method='text').decode("utf-8")
    return inner_trim(text)
