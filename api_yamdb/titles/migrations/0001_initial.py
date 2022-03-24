# Generated by Django 2.2.16 on 2022-03-24 13:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('slug', models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(message='Error invalid slug', regex='^[-a-zA-Z0-9_]+$')])),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('slug', models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(message='Error invalid slug', regex='^[-a-zA-Z0-9_]+$')])),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('year', models.IntegerField(default=None, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2022)])),
                ('description', models.TextField(blank=True, null=True)),
                ('rating', models.IntegerField(default=0)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='titles.Category')),
                ('genre', models.ManyToManyField(related_name='titles', to='titles.Genre')),
            ],
        ),
    ]
