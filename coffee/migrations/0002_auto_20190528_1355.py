# Generated by Django 2.2 on 2019-05-28 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='order_status',
            field=models.CharField(choices=[('Receive', 'Receive'), ('Preparing', 'Preparing'), ('Done', 'Done'), ('Remove', 'Remove')], max_length=255),
        ),
    ]
