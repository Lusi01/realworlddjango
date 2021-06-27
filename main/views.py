from django.shortcuts import render
from django.views.generic import TemplateView

from events.models import Event, Review


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_list'] = Event.objects.all().order_by('-pk')[:3]
        context['review_list'] = Review.objects.all().order_by('-pk')[:3]
        context['special_content'] = True
        return context

