# Generated by Django 3.0.5 on 2020-05-20 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('myblog', '0002_auto_20200520_0632'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('name', models.CharField(default='新用户', max_length=30)),
                ('sexy', models.IntegerField(default=1)),
                ('intro', models.CharField(blank=True, max_length=400)),
            ],
        ),
    ]
