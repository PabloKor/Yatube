from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def uglify(text: str):
    """
    Написать фильтр который меняет четные и нечетные символы на upper(), lower()
    """
    new = ''
    for index in range(len(text)):
        if index % 2 == 0:
            new += text[index].upper()
        else:
            new += text[index].lower()
    return new