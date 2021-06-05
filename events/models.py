from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=90, default='', verbose_name='Категория')

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

    def __str__(self):
        return self.title

    def display_event_count(self):
        return self.events.count()
    display_event_count.short_description = 'Количество событий'


class Feature(models.Model):
    title = models.CharField(max_length=200, default='', verbose_name='Свойство')

    class Meta:
        verbose_name_plural = 'Свойства события'
        verbose_name = 'Свойство события'

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=200, default='', verbose_name='Название')
    description = models.TextField(default='', verbose_name='Описание')
    date_start = models.DateTimeField(verbose_name='Дата начала')
    participants_number = models.PositiveSmallIntegerField(verbose_name='Количество участников')
    is_private = models.BooleanField(default=False, verbose_name='Частное')
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, related_name='events')
    features = models.ManyToManyField(Feature, related_name='свойства')
    logo = models.ImageField(upload_to='events/list', blank=True, null=True)

    @property
    def logo_url(self):
        return self.logo.url if self.logo else f'{settings.STATIC_URL}images/svg-icon/event.svg'

    def get_absolute_url(self):
        return reverse('events:event_detail', args=[str(self.pk)])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'События'
        verbose_name = 'Событие'

    @property
    def rate(self):
        query_set_ratings = self.reviews.values_list('rate', flat=True)
        rates = sum(query_set_ratings) / query_set_ratings.count()
        return round(rates, 1)
    #rate.short_description = 'Средний рэйтинг'

    @property
    def features_list(self):
        list = []
        for el in self.features.get_queryset():
            list.append(el.title)
        return list

    def display_enroll_count(self):
        return self.enrolls.count()
    display_enroll_count.short_description = 'Количество записей'

    def display_places_left(self):
        available = (self.participants_number - self.enrolls.count())
        value = ''
        if available == 0:
            value = str(available) + ' (sold-out)'
        elif available <= (self.participants_number / 2) and available != 0:
            value = str(available) + ' (>50%)'
        elif available > (self.participants_number / 2):
            value = str(available) + ' (<= 50%)'
        return value
    display_places_left.short_description = 'Осталось мест'


class Enroll(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='enrolls')
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE, related_name='enrolls')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    def __str__(self):
        return f'{self.event} - {self.user}'

    class Meta:
        verbose_name_plural = 'Записи на события'
        verbose_name = 'Запись на событие'


class Review(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='reviews')
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE, related_name='reviews')
    rate = models.PositiveSmallIntegerField(null=True, verbose_name='Оценка пользователя')
    text = models.TextField(verbose_name='Текст отзыва')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата отзыва')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name_plural = 'Отзывы на события'
        verbose_name = 'Отзыв на событие'

    def __str__(self):
        return f'{self.user} - {self.event}'
