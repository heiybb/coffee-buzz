# Generated by Django 2.2 on 2019-04-18 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20190418_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='input_name',
            field=models.CharField(default='C', max_length=255),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(choices=[('Coffee bean', 'Coffee bean'), ('Full Cream Milk', 'Full Cream Milk'), ('White Bread', 'White Bread'), ('Black Tea', 'Black Tea'), ('Slim Milk', 'Slim Milk')], max_length=255),
        ),
    ]
