# Generated by Django 3.0.5 on 2020-05-26 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0003_auto_20200526_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='orderedby',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
