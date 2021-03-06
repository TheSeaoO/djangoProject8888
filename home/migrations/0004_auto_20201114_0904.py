# Generated by Django 2.1.8 on 2020-11-14 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20201114_0903'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='bottle_content',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='bottle_title',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.CharField(default=1, max_length=100, verbose_name='回复内容'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bottle',
            name='bottle_content',
            field=models.CharField(max_length=100, verbose_name='漂流瓶内容'),
        ),
        migrations.AlterField(
            model_name='bottle',
            name='bottle_title',
            field=models.CharField(max_length=30, verbose_name='漂流瓶名字'),
        ),
    ]
