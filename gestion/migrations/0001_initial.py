# Generated by Django 2.1.1 on 2018-10-20 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tecnico',
            fields=[
                ('dni', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=50)),
                ('telefono', models.IntegerField()),
                ('mail', models.CharField(max_length=50)),
                ('usuario', models.CharField(max_length=10)),
                ('contrasenia', models.CharField(max_length=30)),
            ],
        ),
    ]
