from decimal import Decimal

from django import template

from urllib.parse import urlparse
from urllib.parse import urlunparse
from django.http import QueryDict

register = template.Library()


@register.simple_tag
def replace_query_param(url, attr, val):
    """
    url의 get parameter에 attr=val 을 넣어줌

    Args:
        url: link url
        attr: parameter name
        val: parameter value

    Returns:

    """
    (scheme, netloc, path, params, query, fragment) = urlparse(url)
    query_dict = QueryDict(query).copy()
    query_dict[attr] = val
    query = query_dict.urlencode()
    return urlunparse((scheme, netloc, path, params, query, fragment))


@register.filter(is_safe=True)
def money_1k(value):
    """
    integer

    Args:
        value:

    Returns:

    """
    if isinstance(value, (int, float, Decimal)):
        value = int(value) // 1000
        return '{0:,}'.format(value)
    else:
        return value


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def percentage(value):
    return '{0:.2f}%'.format(value)


@register.filter
def precision2(value):
    try:
        value = float(value)
        return '{0:,.2f}'.format(value)
    except Exception:
        return value
