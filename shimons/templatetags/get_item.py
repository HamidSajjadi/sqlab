from django import template

register = template.Library()


@register.filter
def getitem(dictionary, key):
    return dictionary.get(key)


@register.filter
def putunderline(inp):
    return inp.replace(' ', '_')


@register.filter
def firstkey(keys_value):
    keys_value = list(keys_value)
    keys_value.sort()
    return keys_value[0]
