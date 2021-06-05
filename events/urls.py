from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [ #имя - именно такое!
    #path('index/', views.index),
    path('list/', views.event_list, name='event_list'),
    path('detail/<int:pk>/', views.event_detail, name='event_detail'),

    path('create/', views.create_event, name='create_event'),

    #path('brand-detail/<int:pk>', views.brand_detail, name='brand_detail'),
]
