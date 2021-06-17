from django.urls import path
from django.views.decorators.http import require_POST
from . import views

app_name = 'events'

urlpatterns = [
    #path('index/', views.index),
    path('list/', views.EventListView.as_view(), name='event_list'),
    path('detail/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event-enroll/', require_POST(views.EventEnrollView.as_view()), name='event_enroll'),

    path('create/', views.EventCreateView.as_view(), name='create_event'),
    path('event-update/<int:pk>/', views.EventUpdateView.as_view(), name='event_update'),

    path('event-participants/<int:pk>/', views.EventParticipantsView.as_view(), name='event_participants'),
    path('event-reviews/<int:pk>/', views.EventReviewsView.as_view(), name='event_reviews'),
    path('event-delete/<int:pk>/', views.EventDeleteView.as_view(), name='event_delete'),
    path('favorite-creation/', require_POST(views.FavoriteCreationView.as_view()), name='favorite_creation'),
    path('error/', views.error, name='error_message')
]
