# Generated by Django 3.2.11 on 2022-04-28 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShipDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipImo', models.IntegerField(unique=True)),
                ('shipName', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='ShipLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logDateTime', models.DateTimeField(default='1970-01-01 00:00:10')),
                ('logCategory', models.CharField(max_length=25)),
                ('logDescription', models.CharField(max_length=100)),
                ('logImo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mclogapp.shipdetails')),
            ],
            options={
                'ordering': ['logDateTime'],
            },
        ),
    ]
