# Generated by Django 4.2.4 on 2023-08-19 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheques', '0003_cheque_created_by_cheque_updated_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cheque',
            name='returned_other',
        ),
    ]
