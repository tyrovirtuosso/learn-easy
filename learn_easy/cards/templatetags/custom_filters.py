from django import template

register = template.Library()

@register.filter
def filter_exclude_default(decks):
    return [deck for deck in decks if deck.deck_name != 'default']
