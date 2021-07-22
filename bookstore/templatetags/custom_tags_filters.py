import datetime
import random

from better_profanity import profanity

from bookstore.models import Book

from django import template
from django.core.cache import cache

import requests

register = template.Library()


@register.filter
def currency(value, name='UAH'):
    return f'{value}, {name}'


# @register.filter
# def no_swear(value):
#     word_list = [
#         'boor', 'heifer', 'homosexual', 'kike', 'layabout', 'lazy', 'slob', 'prat', 'psycho', 'shithead', 'sucker',
#         'twit', 'yob', 'arse', 'crap', 'damn', 'bitch', 'bullshit', 'shit', 'cock', 'dick', 'pussy', 'fuck', 'cunt'
#     ]
#
#     for word in word_list:
#         swear = '*' * len(word)
#         result = value.replace(word, swear)
#         value = result
#     return value


@register.filter(name='no_swear')
def no_swear(value):
    return profanity.censor(value)


@register.filter
def check_forbidden_words(word):
    # Checks if list of forbidden words in the cache
    forbidden_words = cache.get('forbidden_words')
    if forbidden_words is None:
        # Gets the list of forbidden words
        forbidden_words = requests.get('https://random-word-api.herokuapp.com/word?number=100').text
        cache.set('forbidden_words', forbidden_words, 10)
    # Checks if our word in forbidden list of words
    if word in forbidden_words:
        word.replace(word, '*' * len(word))
    return word


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


@register.simple_tag
def random_best_book():
    best_books = Book.objects.filter(rating=10)
    return random.choice(best_books)


@register.simple_tag
def random_book():
    book = Book.objects.order_by('?').first()
    return f'Random book: {book.name}'
