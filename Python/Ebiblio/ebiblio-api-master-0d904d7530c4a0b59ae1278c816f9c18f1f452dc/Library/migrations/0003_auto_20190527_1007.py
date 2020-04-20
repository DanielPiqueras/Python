# Generated by Django 2.2.1 on 2019-05-27 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0002_book_last_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='last_user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL),
        ),
    ]