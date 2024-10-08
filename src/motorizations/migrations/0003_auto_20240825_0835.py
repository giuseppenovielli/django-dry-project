# Generated by Django 3.2 on 2024-08-25 08:35

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('motorizations', '0002_auto_20240628_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caruser',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_user_car', to='motorizations.car', verbose_name='Car'),
        ),
        migrations.AlterField(
            model_name='caruser',
            name='number_plate',
            field=models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Z]*$')], verbose_name='Number plate'),
        ),
        migrations.AlterField(
            model_name='caruser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_user_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
