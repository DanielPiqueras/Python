# Generated by Django 2.2.1 on 2019-05-29 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0005_auto_20190528_0950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='available_book',
        ),
    ]
