# Generated by Django 3.0.4 on 2020-03-26 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_banco'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='banco',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app1.Banco'),
        ),
    ]