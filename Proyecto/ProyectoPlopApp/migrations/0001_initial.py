# Generated by Django 4.0.5 on 2022-07-27 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('lugar', models.CharField(max_length=100)),
                ('imagen', models.ImageField(upload_to='eventos/')),
                ('link_compra', models.URLField(blank=True)),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
            },
        ),
    ]
