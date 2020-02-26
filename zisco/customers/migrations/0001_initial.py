# Generated by Django 2.2.7 on 2020-02-24 13:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0003_auto_20200122_1509'),
        ('users', '0005_auto_20200224_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='Req',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='users.Customer')),
            ],
            options={
                'verbose_name': 'product request',
                'verbose_name_plural': 'product requests',
            },
        ),
        migrations.CreateModel(
            name='ReqItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('qty', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested', to='products.Product')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='customers.Req')),
            ],
            options={
                'verbose_name': 'request item',
                'verbose_name_plural': 'request items',
            },
        ),
    ]
