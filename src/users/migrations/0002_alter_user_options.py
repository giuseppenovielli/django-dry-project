# Generated by Django 3.2 on 2024-06-28 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-id'], 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
