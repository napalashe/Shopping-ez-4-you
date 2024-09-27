from django.shortcuts import render
from item.models import Item, Category
from django.http import HttpResponse
from django.conf import settings


def home(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {"categories": categories, "items": items})


