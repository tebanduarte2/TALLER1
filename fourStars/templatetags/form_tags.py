from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter(name='add_placeholder')
def add_placeholder(field, placeholder_text):
    return field.as_widget(attrs={"placeholder": placeholder_text})
