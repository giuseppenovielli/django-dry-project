# Generated by Django 3.2 on 2023-12-29 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('motorizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car_user',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='car',
            name='engine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motorizations.engine', verbose_name='Engine'),
        ),
        migrations.AlterUniqueTogether(
            name='car_user',
            unique_together={('car', 'user', 'number_plate')},
        ),
    ]
