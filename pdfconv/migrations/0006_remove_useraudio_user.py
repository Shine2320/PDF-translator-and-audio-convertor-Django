# Generated by Django 4.0.6 on 2022-07-29 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdfconv', '0005_rename_pdffilemerger_userpdf_pdffile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraudio',
            name='user',
        ),
    ]
