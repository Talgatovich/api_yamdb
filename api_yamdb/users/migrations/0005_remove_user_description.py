# Generated by Django 2.2.16 on 2022-03-19 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='description',
        ),
    ]