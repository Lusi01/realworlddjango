from django.urls import path
from django.views.decorators.http import require_POST
from . import views

app_name = 'events'

urlpatterns = [
    path('list/', views.EventListView.as_view(), name='event_list'),
    path('detail/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('create/', views.EventCreateView.as_view(), name='create_event'),
    path('event-update/<int:pk>/', views.EventUpdateView.as_view(), name='event_update'),
    path('event-delete/<int:pk>/', views.EventDeleteView.as_view(), name='event_delete'),

    path('enroll-creation/', require_POST(views.EnrollCreationView.as_view()), name='enroll_creation'),
    path('favorite-creation/', require_POST(views.FavoriteCreationView.as_view()), name='favorite_creation'),

    path('error/', views.error, name='error_message')
]
