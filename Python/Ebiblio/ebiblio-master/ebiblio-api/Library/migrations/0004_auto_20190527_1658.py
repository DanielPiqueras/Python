# Generated by Django 2.2.1 on 2019-05-27 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0003_auto_20190527_1007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='history',
            old_name='uuid_Loan',
            new_name='uuid_loan',
        ),
    ]
