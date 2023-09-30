# Generated by Django 4.2.4 on 2023-09-30 02:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cheque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cheque', models.FileField(blank=True, null=True, upload_to='cheques')),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_debited', models.DateField()),
                ('chq_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='cheque amount')),
                ('journal', models.CharField(blank=True, max_length=255)),
                ('cheque_date', models.DateField()),
                ('cheque_no', models.CharField(max_length=255, verbose_name='cheque number')),
                ('receipt_no', models.CharField(blank=True, max_length=255, verbose_name='receipt number')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('date_debited',),
            },
        ),
        migrations.CreateModel(
            name='ChequeStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('desc', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Ministry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Ministries',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=255)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('address1', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Returned',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'returns',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ChequeComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cheque', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comments', to='cheques.cheque')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comment_created', to=settings.AUTH_USER_MODEL)),
                ('upated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comment_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.AddField(
            model_name='cheque',
            name='cheque_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cheque_statuses', to='cheques.chequestatus'),
        ),
        migrations.AddField(
            model_name='cheque',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cheques_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cheque',
            name='ministry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cheques.ministry'),
        ),
        migrations.AddField(
            model_name='cheque',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cheques', to='cheques.owner'),
        ),
        migrations.AddField(
            model_name='cheque',
            name='returned',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cheques.returned'),
        ),
        migrations.AddField(
            model_name='cheque',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cheques_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]
