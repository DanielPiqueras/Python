# Generated by Django 2.2.1 on 2019-06-04 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0007_remove_book_last_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.RemoveField(
            model_name='book',
            name='description',
        ),
        migrations.RemoveField(
            model_name='book',
            name='editorial',
        ),
        migrations.RemoveField(
            model_name='book',
            name='language',
        ),
        migrations.RemoveField(
            model_name='book',
            name='title',
        ),
    ]