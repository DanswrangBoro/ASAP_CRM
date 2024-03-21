from django import template

register = template.Library()

@register.simple_tag
def set_data(booking_id):
    return booking_id
