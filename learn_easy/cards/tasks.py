from celery import shared_task
from .models import Card, Tag
from openai_API.api import OpenAI_API
from django.db.models import Q


ai = OpenAI_API()


@shared_task
def check_and_update_empty_cards():
    print("in check_and_update_empty_cards")
    empty_cards = Card.objects.filter(Q(card_content_system_generated__isnull=True) | Q(card_content_system_generated=''))
    print(f"empty_cards: {empty_cards}")
    for card in empty_cards:
        update_card_meaning.delay(card.pk)

@shared_task
def update_card_meaning(pk):
    card = Card.objects.get(pk=pk)    
    card_name = card.card_name
    print(f"in update_card_meaning for {card_name}")
    # meaning = "Sample Meaning"
    meaning = ai.get_meaning(card_name)
    card.card_content_system_generated = meaning
    card.save()
    print(f"update_card_meaning done for {card_name}!")
    
@shared_task
def update_card_tags(pk):    
    card = Card.objects.get(pk=pk)
    card_name = card.card_name
    print(f"in update_card_tags for {card_name}")
    # tag = ['TEST1', 'TEST2']
    tags = ai.get_category(card_name)
    # card.system_defined_tags.clear()
    
    for tag_name in tags:            
        tag_name = tag_name.upper()
        tag, created = Tag.objects.get_or_create(tag_name=tag_name)  
        if created:
            tag.save()
        card.system_defined_tags.add(tag)
    
    card.save()
    print(f"update_card_tags done for {card_name}!")