# Generated by Django 4.0.5 on 2022-08-02 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoPlopApp', '0005_imagenesevento_delete_multiple'),
    ]

    operations = [
        migrations.CreateModel(
            name='FondoPagina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('aprobado', models.BooleanField(default=False)),
                ('imagen', models.ImageField(upload_to='imagenes/')),
            ],
            options={
                'verbose_name': 'Fondo',
                'verbose_name_plural': 'Fondos',
            },
        ),
    ]
