from django.db import models


class UsersForPath(models.Model):
    username = models.CharField(verbose_name='Usuário', max_length=100)


class Paths(models.Model):
    username = models.ForeignKey(UsersForPath, on_delete=models.CASCADE)
    startpointpath = models.CharField(verbose_name='Caminho de ponto de partida.', max_length=500)
