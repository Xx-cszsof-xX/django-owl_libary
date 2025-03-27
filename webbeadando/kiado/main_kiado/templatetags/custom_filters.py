from django import template

register = template.Library()

@register.filter(name='format_currency')
def format_currency(value):
    try:
        value = float(value)
        return f"{value:,.0f} Ft".replace(",", " ")
    except (ValueError, TypeError):
        return value
