from django.db import models
from mail.manager import SubscriberQuerySet


class Subscriber(models.Model):
    email = models.EmailField(null=True)
    objects = SubscriberQuerySet.as_manager()

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    @staticmethod
    def get_by_email(email):
        return Subscriber.objects.filter(email__iexact=email).first()

    @staticmethod
    def get_objects_list():
        qs = Subscriber.objects.with_counts()
        subscribers = []
        for item in qs:
            subscribers.append({
                'email': item.email,
                'letter_count': item.letter_count,
                'sent_letter_count': item.sent_letter_count,
            })
        return subscribers


class Letter(models.Model):
    to = models.ForeignKey(Subscriber, null=True, on_delete=models.CASCADE, verbose_name='Получатель',
                           related_name='letters')
    subject = models.CharField(max_length=200, default='', verbose_name='Тема письма')
    text = models.TextField(default='', verbose_name='Текст письма')
    is_sent = models.BooleanField(default=False, verbose_name='Отправлено')

    def __str__(self):
        return f'{self.to} - {self.subject}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'

    @staticmethod
    def create_letters(emails, subject, text):
        new_letters = 0
        for email in emails:
            #to = Subscriber.objects.filter(email__iexact=email).first()
            to = Subscriber.get_by_email(email)
            if to:
                Letter.objects.create(to=to, subject=subject, text=text)
                new_letters += 1
        return new_letters


