from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import FileExtensionValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #avatar = models.ImageField(null=True, blank=True, upload_to='accounts/profiles/avatar')
    avatar = models.FileField(null=True, blank=True, upload_to="accounts/profiles/avatar", validators=[
        FileExtensionValidator(['jpg', 'png', 'gif', 'svg'])])
    phone = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        #return reverse('accounts:profile', args=[str(self.pk)])
        #return reverse('accounts:profile', args=[str(self.user.pk)])
        return reverse('accounts:profile')

    @property
    def avatar_url(self):
        return self.avatar.url if self.avatar else ''
