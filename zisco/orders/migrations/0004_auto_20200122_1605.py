# Generated by Django 2.2.7 on 2020-01-22 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_quotation_quotationitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationitem',
            name='_price',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=19),
        ),
    ]