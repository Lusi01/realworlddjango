# Generated by Django 3.2.1 on 2021-06-15 08:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0007_event_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='events.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='event',
            name='features',
            field=models.ManyToManyField(related_name='свойства', to='events.Feature', verbose_name='Особенности'),
        ),
        migrations.AlterField(
            model_name='event',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='events/list', verbose_name='Загрузить изображение'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='events.event')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
