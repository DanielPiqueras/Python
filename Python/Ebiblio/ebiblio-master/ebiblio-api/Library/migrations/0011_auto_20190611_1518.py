# Generated by Django 2.2.1 on 2019-06-11 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0010_history_reserved_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='editorial',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='title',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
