from django.core.paginator import Paginator
from django.db.models import Prefetch, Count, F
from django.template.defaultfilters import length
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseForbidden, Http404, QueryDict

from events.forms import (EventCreationForm,
                          EventUpdateForm,
                          EnrollCreationForm,
                          FavoriteCreationForm,
                          EventFilterForm)
from events.models import Category, Event, Feature, Review, Enroll, Favorite
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import json



class MyLoginRequiredMixin:
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # выдается сообщение об ошибке с кодом status_code = 403:
            return HttpResponseForbidden('Недостаточно прав')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # выдается сообщение об ошибке с кодом status_code = 403:
            return HttpResponseForbidden('Недостаточно прав')
        return super().post(request, *args, **kwargs)


def error(request):
    template_name =  'events/error_message.html'
    context = {
        'title': 'Ошибка'
    }
    return render(request, template_name, context)


def index(request):
    template_name = 'events/index.html'
    context = {}
    return render(request, template_name, context)


def hello(request):
    return HttpResponse('Hello, World!')



class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html' # необязательно, указать, если имя шаблона отличается от стандартного
    context_object_name = 'event_objects'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = EventFilterForm(self.request.GET)
        return context

    def get_queryset(self):

        queryset = super().get_queryset()
        queryset = queryset.EvQuSet()

          # обработка кнопки "Сбросить"
        if self.request.GET.get('Delete', ''):
            filter_dist = self.request.GET.copy()
            # удалить 'filter' в сесии:
            if 'filter' in self.request.session:
                del self.request.session['filter']

            # удаоить фильтры в запросах GET:
            if 'date_start' in filter_dist:
                del filter_dist['date_start']
            if 'date_end' in filter_dist:
                del filter_dist['date_end']
            if 'category' in filter_dist:
                del filter_dist['category']
            if 'features' in filter_dist:
                del filter_dist['features']
            if 'is_private' in filter_dist:
                del filter_dist['is_private']
            if 'is_available' in filter_dist:
                del filter_dist['is_available']
            if 'page' in filter_dist:
                del filter_dist['page']
            if 'Delete' in filter_dist:
                del filter_dist['Delete']

            self.request.GET = filter_dist

            return queryset.order_by('-pk')

        # начало обработки запроса GET для запоминариня фильтров
        filter_dist = {}
        # если был переход по стриницам
        page = self.request.GET.get('page', None)

        if 'filter' in self.request.session:
            filter_dist = self.request.session['filter']

            if page:
                #добавить 'page' к session['filter']
                filter_dist.update({'page': page})
            else:
                if self.request.GET:
                    # поностью обновить session['filter']
                    del self.request.session['filter']
                    filter_dist = self.request.GET.copy()

            if len(filter_dist) > 0:
                self.request.session['filter'] = filter_dist
                self.request.GET = filter_dist
        else:
            filter_dist = self.request.GET.copy()
        # конец обработки запроса GET для запоминариня фильтров

        # обработка фильтров
        if filter_dist.__contains__('category'):
            filter_category = self.request.GET.get('category', '')
            filter_dist['category'] = filter_category
        else:
            filter_category = None

        if filter_dist.__contains__('features'):
            q = json.loads(json.dumps(dict(filter_dist)))
            filter_features = q['features']
            filter_dist['features'] = filter_features
        else:
            filter_features = None

        if filter_dist.__contains__('date_start'):
            filter_date_start = self.request.GET.get('date_start', '')
            filter_dist['date_start'] = filter_date_start
        else:
            filter_date_start = None

        if filter_dist.__contains__('date_end'):
            filter_date_end = self.request.GET.get('date_end', '')
            filter_dist['date_end'] = filter_date_end
        else:
            filter_date_end = None

        if filter_dist.__contains__('is_private'):
            filter_is_private = self.request.GET.get('is_private', '')
            filter_dist['is_private'] = filter_is_private
        else:
            filter_is_private = None

        if filter_dist.__contains__('is_available'):
            filter_is_available = self.request.GET.get('is_available', '')
            filter_dist['is_available'] = filter_is_available
        else:
            filter_is_available = None

        if page:
            filter_dist['page'] = page

        if len(filter_dist) > 0:
            self.request.session['filter'] = filter_dist

        if filter_category:
            queryset = queryset.filter(category=filter_category)
        if filter_features:
            for feature in filter_features:
                queryset = queryset.filter(features__in=feature)
        if filter_date_start:
            queryset = queryset.filter(date_start__gt=filter_date_start)
        if filter_date_end:
            queryset = queryset.filter(date_start__lt=filter_date_end)
        if filter_is_private:
            queryset = queryset.filter(is_private=True)
        if filter_is_available:
            queryset = queryset.filter(available__gt=0)

        return queryset.order_by('-pk')




class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'events/event_update.html'
    form_class = EventCreationForm

    success_url = reverse_lazy('events:event_list') #переход в случае успеха. По умолчанию, если не указать -
    # переход на детальную страницу

    def form_valid(self, form):
        messages.success(self.request, 'Новое событие создано успешно')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)



class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    template_name = 'events/event_update.html'
    form_class = EventUpdateForm

    def get_context_data(self, **kwargs):
        event = self.object
        context = super().get_context_data(**kwargs)

        return context

    def get_queryset(self):

        pk = self.kwargs.get(self.pk_url_kwarg)
        queryset = super().get_queryset().filter(pk=pk)
        queryset = queryset.EvQuSet()
        return queryset



class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event #queryset по умолчанию
    success_url = reverse_lazy('events:event_list')

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f'Событие {self.object} удалено')
        return result



class EnrollCreationView(LoginRequiredMixin, CreateView ):
    model = Enroll
    form_class = EnrollCreationForm

    def get_success_url(self):
        return self.object.event.get_absolute_url()

    def form_valid(self, form):
        messages.success(self.request,
                         f'В событие добавлена запись')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        event = form.cleaned_data.get('event', None)
        user = form.cleaned_data.get('user', None)
        if not user:
            return HttpResponseForbidden('Недостаточно прав')

        if not event:
            event = get_object_or_404(Event, pk=form.data.get('event'))
        redirect_url = event.get_absolute_url() if event else reverse_lazy('events:event_list')
        return HttpResponseRedirect(redirect_url)




class FavoriteCreationView(LoginRequiredMixin, CreateView):
    model = Favorite
    form_class = FavoriteCreationForm

    def get_success_url(self):
        return self.object.event.get_absolute_url()

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        event = form.cleaned_data.get('event', None)

        user = form.cleaned_data.get('user', None)
        if not user:
            return HttpResponseForbidden('Недостаточно прав')

        if not event:
            event = get_object_or_404(Event, pk=form.data.get('event'))
        redirect_url = event.get_absolute_url() if event else reverse_lazy('events:event_list')
        return HttpResponseRedirect(redirect_url)


    def form_valid(self, form):
        messages.success(self.request,
                         f'Событие добавлено в избранное')
        return super().form_valid(form)



class EventDetailView(DetailView):
    model = Event

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        initial = {
            'user': self.request.user,
            'event': self.object,
        }

        context['enroll_form'] = EnrollCreationForm(initial=initial)
        context['favorite_form'] = FavoriteCreationForm(initial=initial)

        return context

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        queryset = super().get_queryset().filter(pk=pk)
        queryset = queryset.EvQuSet()

        return queryset


@require_POST
def create_review(request):

    rate = ''
    text = ''
    created = ''
    user_name = ''
    ok = True
    msg = ''

    event_id = request.POST.get('event_id')
    rate = request.POST.get('rate')
    text = request.POST.get('text')
    user_req = request.user

    if not request.user.is_authenticated:
        user_req = None
        ok = False
    else:
        user_name = user_req.__str__()

    event = Event.objects.get(pk=event_id)
    created = datetime.date.today().strftime('%d.%m.%Y')

    if Review.objects.filter(user=user_req, event=event).exists():
        msg = 'Вы уже отправляли отзыв к этому событию'
        ok = False

    elif not event:
        msg = 'Событие, на которое отправляете комментарий, не найдено!'
        ok = False

    elif text == '' or rate == '':
        msg = 'Оценка и текст отзыва - обязательные поля'
        ok = False

    elif user_req and user_req.is_authenticated:
        # добавляем в БД
        try:
            element = Review(
                user = user_req,
                event = event,
                rate = rate,
                text = text,
                # created = created,
                # updated = created
            )
            element.save()

        except:
            msg = 'комментарий не удалось сохранить в БД! '
            ok = False

    else:
        msg = 'Отзывы могут отправлять только зарегистрированные пользователи'
        ok = False

    form_data = {
        'ok': ok,  # True, если отзыв создан успешно
        'msg': msg,  # Сообщение об ошибке
        'rate': rate,  # оценка, - обязательно
        'text': text,  # текст отзыва - обязательно
        'created': created,  # Дата создания отзыва в формате DD.MM.YYYY
        'user_name': user_name # 'admin'  # user_name, #Полное имя пользователя
    }

    return JsonResponse(form_data)
