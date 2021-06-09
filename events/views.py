import datetime
import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse

from events.models import Category, Event, Feature, Review
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST


def index(request):
    return HttpResponse('Hello, World!')


def event_list(request):
    template_name = 'events/event_list.html'
    event_objects = Event.objects.all()
    event_number = event_objects.count()

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
    caption = 'Записаться'
    if available < 1:
        attr = 'disabled'
        caption = 'Мест нет'


    context = {
        'event': event,
        'reviews': reviews,
        'available': available,
        'attr': attr,
        'caption': caption
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

    #event = get_object_or_404(Event, pk=event_id)
    event = Event.objects.get(pk=event_id)
    created = datetime.date.today().strftime('%d.%m.%Y')

    if Review.objects.filter(user=user_req):
        msg = 'Вы уже отправляли отзыв к этому событию'
        ok = False

    if not event:
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
        # finally:
        #     msg = msg + ' Отправлено!'

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
    #print(formData)

    #return HttpResponse(json.dumps(formData))
    return JsonResponse(formData)
