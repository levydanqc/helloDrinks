# Generated by Django 4.0.1 on 2022-02-07 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alcool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('pseudo', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('adresse', models.CharField(max_length=100)),
                ('ddn', models.DateField()),
                ('alcoolPref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helloDrinks.alcool')),
            ],
        ),
        migrations.CreateModel(
            name='DrinkHistorique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('drink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helloDrinks.drink')),
                ('usager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helloDrinks.usager')),
            ],
        ),
    ]
