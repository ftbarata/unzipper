from django.db import models


class UsersForPath(models.Model):
    username = models.CharField(verbose_name='Usuário', max_length=100)

    class Meta:
        verbose_name = 'Usuários para caminhos'
        verbose_name_plural = 'Usuários para caminhos'

    def __str__(self):
        return self.username

class Paths(models.Model):
    username = models.ForeignKey(UsersForPath, on_delete=models.CASCADE)
    startpointpath = models.CharField(verbose_name='Caminho de ponto de partida.', max_length=500)

    class Meta:
        verbose_name = 'Caminho'
        verbose_name_plural = 'Caminhos'

    def __str__(self):
        return self.startpointpath + "   ({})".format(str(self.username))