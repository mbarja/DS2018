# Generated by Django 2.1.1 on 2018-11-19 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0020_mantenimiento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.BigIntegerField(),
        ),
    ]