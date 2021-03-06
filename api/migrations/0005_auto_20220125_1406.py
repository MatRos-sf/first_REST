# Generated by Django 3.2.11 on 2022-01-25 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20220125_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extrainfo',
            name='rodzaj',
            field=models.IntegerField(choices=[(0, 'Sci-fi'), (0, 'Nieznane'), (0, 'Drama'), (0, 'Horror'), (0, 'Komedia')], default=0),
        ),
        migrations.AlterField(
            model_name='recenzja',
            name='film',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recenzje', to='api.film'),
        ),
        migrations.CreateModel(
            name='Aktor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imie', models.CharField(max_length=32)),
                ('nazwisko', models.CharField(max_length=32)),
                ('filmy', models.ManyToManyField(to='api.Film')),
            ],
        ),
    ]
