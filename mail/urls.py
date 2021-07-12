from django.urls import path
from . import views

app_name = 'mail'

urlpatterns = [
    path('subscriber/create/', views.SubscriberCreateView.as_view(), name='subscriber_create'),
    path('subscriber/list/', views.SubscriberListView.as_view(), name='subscriber_list')
]