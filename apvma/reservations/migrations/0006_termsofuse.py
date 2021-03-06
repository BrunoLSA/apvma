# Generated by Django 2.0 on 2018-01-20 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0005_auto_20180114_1842'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermsOfUse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='reservations/termsofuse/')),
                ('uploaded_on', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
            ],
            options={
                'verbose_name': 'Regras de Uso de Ambiente',
                'verbose_name_plural': 'Regras de Uso de Ambiente',
            },
        ),
    ]
