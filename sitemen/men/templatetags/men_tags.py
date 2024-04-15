from django import template
from django.db.models import Count

import men.views as views
from men.models import Category, TagPost
from men.utils import menu

register = template.Library()

@register.inclusion_tag('men/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count('posts')).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('men/list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0)}

@register.simple_tag
def get_menu():
    return menu