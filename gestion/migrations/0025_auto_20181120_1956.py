# Generated by Django 2.1.1 on 2018-11-20 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0024_delete_tipousuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alquiler',
            name='estado',
            field=models.CharField(choices=[('R', 'Reservado'), ('C', 'Confirmado'), ('S', 'Esperando Confirmacion'), ('E', 'En curso'), ('O', 'Cancelado'), ('F', 'Finalizado')], max_length=1),
        ),
    ]
