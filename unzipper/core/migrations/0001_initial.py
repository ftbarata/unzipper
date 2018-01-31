# Generated by Django 2.0.1 on 2018-01-31 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paths',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startpointpath', models.CharField(max_length=500, verbose_name='Caminho de ponto de partida.')),
            ],
        ),
        migrations.CreateModel(
            name='UsersForPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, verbose_name='Usuário')),
            ],
        ),
        migrations.AddField(
            model_name='paths',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UsersForPath'),
        ),
    ]