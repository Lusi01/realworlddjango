from django.http import JsonResponse
from django.views.decorators.http import require_POST


from mail.models import Subscriber, Letter
from realworlddjango.settings import env
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.db.models import F
from threading import Thread
import datetime


@require_POST
def create_letters_view(request):
    emails = request.POST.getlist('email', None)
    subject = request.POST.getlist('subject', '')[0]
    text = request.POST.getlist('text', '')[0]
    if emails and subject and text:
        Letter.create_letters(emails, subject, text)
    return JsonResponse({'subscribers': Subscriber.get_objects_list()})


def send_mails(letter):

    mail = []
    subject = letter.subject.replace('[', '').replace(']', '')
    text = letter.text.replace('[', '').replace(']', '')
    mail.append(letter.mail)

    send_mail(
        subject,
        text,
        env('EMAIL_HOST_USER'),
        mail,
        fail_silently=False,
    )

def portion(pars):

    for letter in pars:
        th = Thread(target=send_mails, args=(letter,))
        th.start()


@require_POST
def send_letters_view(request):
    # получить список неотправленных писем
    list_email_sent = Letter.objects.select_related('to').annotate(
        mail=F('to__email')
    ).filter(is_sent=False).all()

    ids = []
    count = 0
    part = 0
    #start = datetime.datetime.now()

    threads_list = []
    while part < list_email_sent.count():
        for i in range(50):
            if count < list_email_sent.count():
                id = list_email_sent[count].id
                ids.append(id)
                count += 1

        # делить список на заданные порции по 50 шт.
        list = list_email_sent[part:(part+50)]
        pars = list
        part += 50

        th = Thread(target=portion, args=(pars, ))
        th.start()
        threads_list.append(th)

    for thread in threads_list:
        thread.join()

    Letter.objects.filter(id__in=ids).update(is_sent=True)
    #end_total = datetime.datetime.now()
    #print(f'Время выполнения всего: {(end_total - start).total_seconds()} секунд')

    # Обычный режим:
    # Время выполнения: 4.613135 секунд
    # count = 7
    #

    # Многопоточный режим:
    # Время выполнения: 0.091998 секунд
    # count = 7

    # Многопоточный режим с ожиданием завершения потоков без разделения на порции:
    # Время выполнения: 4.646157 секунд
    # count = 7

    #print('count=', count)
    #is_sent = True => отправлено
    # is_sent = False => не отправлено

    return JsonResponse({'subscribers': Subscriber.get_objects_list()})


def get_subscribers_view(request):

    list_email_sent = Letter.objects.filter(is_sent = False).values_list('is_sent', flat=True)
    if list_email_sent:
        all_email_sent = True
    else:
        all_email_sent = False

    return JsonResponse({
        'subscribers': Subscriber.get_objects_list(),
        'all_email_sent': all_email_sent,
    })
