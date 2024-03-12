from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='format_time')
def format_time(value):
    # Convert the input string to a datetime object
    datetime_obj = datetime.fromisoformat(value)
    # Format the datetime object to display only the time part
    time_string = datetime_obj.strftime('%H:%M:%S')
    # Remove the last two characters from the time string
    truncated_time_string = time_string[:-3]
    return truncated_time_string
