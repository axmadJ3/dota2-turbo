from django import template


register = template.Library()

@register.filter
def mmss(value):
    total = int(value)
    minutes = total // 60
    seconds = total % 60
    return f"{minutes}:{seconds:02d}"
