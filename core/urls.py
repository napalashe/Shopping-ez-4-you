from django.urls import path
from core.views import home
from . import views


app_name = "core"

urlpatterns = [
    path("", home, name ='index'),
]