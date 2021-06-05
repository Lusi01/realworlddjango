from django.urls import path
from . import views

app_name = 'api_events'

urlpatterns = [ #имя - именно такое!
    path('reviews/create/', views.create_review, name='create_review'),
]
