# Generated by Django 2.1.8 on 2020-11-14 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20201114_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='bottle',
            name='launch_time',
            field=models.DateTimeField(null=True, verbose_name='投放时间'),
        ),
    ]
