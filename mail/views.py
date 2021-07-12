from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from mail.forms import SubscriberCreateForm, LetterCreateForm
from mail.models import Subscriber


class SubscriberCreateView(LoginRequiredMixin, CreateView):
    model = Subscriber
    form_class = SubscriberCreateForm
    success_url = reverse_lazy('mail:subscriber_list')

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return HttpResponseRedirect(self.success_url)

    def form_valid(self, form):
        messages.success(self.request, 'Подписчик успешно создан')
        return super().form_valid(form)


class SubscriberListView(LoginRequiredMixin, ListView):
    model = Subscriber
    template_name = 'mail/subscribers_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['subscriber_form'] = SubscriberCreateForm()
        context['letter_form'] = LetterCreateForm()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        #return qs.annotate(letter_count=Count('letters'), sent_letter_count=Count('letters'))
        return qs.with_counts()

