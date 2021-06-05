import datetime
import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from events.models import Category, Event, Feature, Review
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST


def index(request):
    return HttpResponse('Hello, World!')


def event_list(request):
    template_name = 'events/event_list.html'
    event_objects = Event.objects.all()
    event_number = Event.objects.all().count()

    category = Category.objects.all()
    feature = Feature.objects.all()

    context = {
        'event_objects': event_objects,
        'event_number': event_number,
        'category': category,
        'feature': feature,
    }
    return render(request, template_name, context)


def event_detail(request, pk):
    template_name = 'events/event_detail.html'
    event = get_object_or_404(Event, pk=pk)
    reviews = []
    for el in event.reviews.values():
        el['user'] = get_object_or_404(User, pk=el['user_id']).__str__()
        reviews.append(el)

    available = event.participants_number - event.enrolls.count()
    attr = ''
    if available < 1:
        attr = 'disabled'

    context = {
        'event': event,
        'reviews': reviews,
        'available': available,
        'attr': attr,
    }
    return render(request, template_name, context)


def create_event(request):
    print(request)

    template_name = 'events/event_update.html'
    msg = 'OK'

    if request.user and request.user.is_authenticated:
        # добавляем в БД
        try:
          pass
        except:
            msg = 'событие не удалось создать! '
        finally:
            msg = msg + ' Событие создано!'
    else:
        msg = 'пользователь не залогинен'

    content = {
        'msg': msg, #Сообщение об ошибке
    }

    return render(request, template_name, content)




@require_POST
def create_review(request):

    msg = ''
    event_id = request.POST.get('event_id')
    event = get_object_or_404(Event, pk=event_id)
    rate = request.POST.get('rate')
    print('rate', rate)
    text = request.POST.get('text')
    print('text', text)
    user_name = request.user
    if not request.user.is_authenticated:
        user_name = None

    created = datetime.date.today().strftime('%d.%m.%Y')
    ok = True

    if Review.objects.filter(user=user_name):
        msg = 'Вы уже отправляли отзыв к этому событию'
        ok = False

    elif text == '' or rate == '':
        msg = 'Оценка и текст отзыва - обязательные поля'
        ok = False

    elif user_name and user_name.is_authenticated:
        # добавляем в БД
        try:
            print('на запись')
            element = Review(
                user = user_name,
                event = event,
                rate = rate,
                text = text,
                created = created,
                updated = created
            )
            element.save()

        except:
            msg = 'комментарий не удалось сохранить в БД! '
        finally:
            msg = msg + ' Отправлено!'
    else:
        msg = 'Отзывы могут отправлять только зарегистрированные пользователи'
        ok = False

    formData = {
        'ok': ok,  # True, если отзыв создан успешно
        'msg': msg,  # Сообщение об ошибке
        'rate': rate,  # оценка, - обязательно
        'text': text,  # текст отзыва - обязательно
        'created': created,  # Дата создания отзыва в формате DD.MM.YYYY
        'user_name': user_name.__str__()  # 'admin'  # user_name, #Полное имя пользователя
    }

    return HttpResponse(json.dumps(formData))
