# Generated by Django 2.2.7 on 2020-02-23 22:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='managers',
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
