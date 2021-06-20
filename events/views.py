from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseForbidden

from events.forms import EventCreationForm, EventUpdateForm, EventEnrollForm, FavoriteCreationForm
from events.models import Category, Event, Feature, Review, Enroll, Favorite
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse_lazy



class LoginRequiredMixin:

    def get(self, request, *args, **kwargs):
        user = request.user
        if not request.user.username:
            # выдается сообщение об ошибке с кодом status_code = 403:
            return HttpResponseForbidden('Не задан user')
        if not request.user.is_authenticated:
            # выдается сообщение об ошибке с кодом status_code = 403:
            return HttpResponseForbidden('Недостаточно прав')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user
        if not request.user.username:
            # выдается сообщение об ошибке с кодом status_code = 403:
            return HttpResponseForbidden('Не задан user')
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



class FavoriteCreationView(LoginRequiredMixin, CreateView):
    model = Favorite

    def post(self, request, *args, **kwargs):
        if not self.request.user.username or not self.request.user.is_authenticated:
            return HttpResponseForbidden('Недостаточно прав FavoriteCreationView')
        return super().post(request, *args, **kwargs)

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



class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html' # необязательно, указать, если имя шаблона отличается от стандартного
    context_object_name = 'event_objects'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.all()
        feature = Feature.objects.all()
        context['event_number'] = Event.objects.count()
        context['category'] = category
        context['feature'] = feature

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
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



class EventParticipantsView(LoginRequiredMixin, DetailView):
    model = Event #queryset по умолчанию
    template_name = 'events/event_participants.html'

    def get_context_data(self, **kwargs):
        event = self.object
        context = super().get_context_data(**kwargs)

        enrolls = self.object.enrolls.all().order_by('user_id')
        reviews = self.object.reviews.all().values('user_id', 'rate').order_by('user_id')

        for el in enrolls:
            el.review = 0
            for rev in reviews:
                if el.user.pk == rev['user_id']:
                    el.review = rev['rate']
                    break

        context['enrolls'] = enrolls

        return context



class EventReviewsView(LoginRequiredMixin, DetailView):
    model = Event #queryset по умолчанию
    template_name = 'events/event_reviews.html'

    def get_context_data(self, **kwargs):
        event = self.object
        context = super().get_context_data(**kwargs)

        reviews = self.object.reviews.all()
        context['reviews'] = reviews

        return context



class EventDeleteView(LoginRequiredMixin, DeleteView):

    model = Event #queryset по умолчанию
    template_name = 'events/event_delete.html'

    success_url = reverse_lazy('events:event_list')

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f'Событие {self.object} удалено')
        return result



class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event

    template_name = 'events/event_update.html'
    form_class = EventUpdateForm



class EventEnrollView(LoginRequiredMixin, CreateView ):
    model = Enroll

    def post(self, request, *args, **kwargs):
        if not self.request.user.username or not self.request.user.is_authenticated:
            return HttpResponseForbidden('Недостаточно прав EventEnrollView')

        return super().post(request, *args, **kwargs)

    form_class = EventEnrollForm

    def get_success_url(self):
        return self.object.event.get_absolute_url()

    def form_valid(self, form):
        messages.success(self.request,
                         f'В событие добавлена запись')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)



class EventDetailView(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        event = self.object
        created = datetime.date.today().strftime('%d.%m.%Y')

        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        context['enrolls_form'] = EventEnrollForm(initial={
            'user': self.request.user,
            'event': self.object,
            'created': created,

        })
        context['favorite_form'] = FavoriteCreationForm(initial={
            'user': self.request.user,
            'event': self.object,
        })
        available = self.object.participants_number - self.object.enrolls.count()

        attr = ''
        attr_for_notuser = ''
        caption = 'Записаться'
        if not self.request.user.username or not self.request.user.is_authenticated:
            attr_for_notuser = 'disabled'
            attr = ''

        if available < 1:
            if attr_for_notuser == '':
                attr = 'disabled'
            caption = 'Мест нет'
        context['attr'] = attr
        context['attr_for_notuser'] = attr_for_notuser
        context['caption'] = caption
        context['available'] = available

        return context



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

    if Review.objects.filter(user=user_req, event=event):
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
                created = created,
                updated = created
            )
            element.save()

        except:
            msg = 'комментарий не удалось сохранить в БД! '
            ok = False

    else:
        msg = 'Отзывы могут отправлять только зарегистрированные пользователи'
        ok = False

    formData = {
        'ok': ok,  # True, если отзыв создан успешно
        'msg': msg,  # Сообщение об ошибке
        'rate': rate,  # оценка, - обязательно
        'text': text,  # текст отзыва - обязательно
        'created': created,  # Дата создания отзыва в формате DD.MM.YYYY
        'user_name': user_name # 'admin'  # user_name, #Полное имя пользователя
    }

    return JsonResponse(formData)
