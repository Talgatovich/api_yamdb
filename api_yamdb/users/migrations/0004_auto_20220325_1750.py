# Generated by Django 2.2.16 on 2022-03-25 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220325_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.TextField(max_length=150, unique=True),
        ),
    ]
