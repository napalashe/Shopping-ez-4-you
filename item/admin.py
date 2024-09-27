from django.contrib import admin
from .models import Category, Item

# Register your models here.
from django.contrib import admin
from .models import Category, Item

admin.site.register(Category)
admin.site.register(Item)