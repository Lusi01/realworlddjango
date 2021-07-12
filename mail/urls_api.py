from django.urls import path
from . import api

app_name = 'api_mail'

urlpatterns = [
    path('create-letters/', api.create_letters_view, name='create_letters'),
]
