from django.http import JsonResponse
from django.views.decorators.http import require_POST

from mail.models import Subscriber, Letter


@require_POST
def create_letters_view(request):
    emails = request.POST.getlist('email', None)
    subject = request.POST.getlist('subject', '')
    text = request.POST.getlist('text', '')
    if emails and subject and text:
        Letter.create_letters(emails, subject, text)

    return JsonResponse({'subscribers': Subscriber.get_objects_list()})

