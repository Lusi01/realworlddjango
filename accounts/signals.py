from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .models import Profile


@receiver(post_save, sender=User) # post_save-вид сигнала, sender-отправитель сигнала
def create_user_profile(**kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        # pk в Profile д.б. = pk в User
        Profile.objects.create(pk=user.pk, user=kwargs['instance'])

