# Generated by Django 2.2.7 on 2020-01-22 13:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0002_order_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='DispatchPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dispatch_plan', to='orders.Order')),
            ],
            options={
                'verbose_name_plural': 'dispatch plans',
            },
        ),
    ]
