# Generated by Django 2.2.16 on 2022-03-21 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0003_title_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
    ]
