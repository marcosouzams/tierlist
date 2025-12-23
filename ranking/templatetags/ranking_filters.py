from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter para acessar item de dicionário por chave
    Uso: {{ dict|get_item:key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def mul_by_ten(value):
    """
    Template filter para multiplicar um valor por 10
    Converte nota de 0-10 para percentual 0-100
    Uso: {{ nota|mul_by_ten }}
    """
    try:
        return float(value) * 10
    except (ValueError, TypeError):
        return 0
