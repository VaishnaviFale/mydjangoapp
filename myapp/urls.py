# myapp/urls.py
from django.urls import path
from .views import hello_world
from .views import MyView

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('metrics/', include('myapp.metrics')),
]

