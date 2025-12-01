from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return None
    if isinstance(dictionary, dict):
        item = dictionary.get(key)
        if item and hasattr(item, '__dict__'):
            return {'score': item.score, 'passed': item.passed}
        return item
    return None
