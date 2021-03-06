# Generated by Django 2.0 on 2018-02-03 23:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20180105_2006'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternalRegiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='core/documents/internal_regiment', validators=[django.core.validators.FileExtensionValidator(['pdf'], 'O sistema só permite o upload de arquivos PDF.')])),
                ('uploaded_on', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
            ],
            options={
                'verbose_name': 'Regimento Interno',
                'verbose_name_plural': 'Regimento Interno',
            },
        ),
    ]
