# Generated by Django 4.0.6 on 2022-07-29 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdfconv', '0002_userpdf_time_useraudio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpdf',
            name='time',
        ),
        migrations.AddField(
            model_name='userpdf',
            name='unique_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]