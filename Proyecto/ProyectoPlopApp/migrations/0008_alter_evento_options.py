# Generated by Django 4.0.5 on 2022-08-06 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoPlopApp', '0007_alter_evento_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='evento',
            options={'ordering': ['-fecha'], 'verbose_name': 'Evento', 'verbose_name_plural': 'Eventos'},
        ),
    ]
