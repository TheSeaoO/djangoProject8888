# Generated by Django 2.1.8 on 2020-11-14 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20201114_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bottle',
            name='pick_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pick_user', to='home.User', verbose_name='捞起人'),
        ),
    ]
