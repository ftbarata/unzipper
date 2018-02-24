from django.db import models


class UsersForPath(models.Model):
    username = models.CharField(verbose_name='Usuário', max_length=100)
    can_change_password = models.BooleanField(verbose_name='Pode alterar a senha', default=False)

    class Meta:
        verbose_name = 'Usuários para caminhos'
        verbose_name_plural = 'Usuários para caminhos'

    def __str__(self):
        return self.username


class PermissionsProfileConfig(models.Model):
    profile_name = models.CharField(verbose_name='Nome do perfil', max_length=20)
    complementary_path = models.CharField(verbose_name='Complemento do caminho', max_length=500)
    owner = models.CharField(verbose_name='Usuário dono', max_length=20)
    group = models.CharField(verbose_name='Grupo dono', max_length=20)

    class Meta:
        verbose_name = 'Configuração de perfil de permissões'
        verbose_name_plural = 'Configurações de perfis de permissões'

    def __str__(self):
        return self.profile_name


class Paths(models.Model):
    username = models.OneToOneField(UsersForPath, on_delete=models.CASCADE)
    permission_profile = models.OneToOneField(PermissionsProfileConfig, on_delete=models.CASCADE)
    startpointpath = models.CharField(verbose_name='Caminho de ponto de partida.', max_length=500)

    class Meta:
        verbose_name = 'Caminho'
        verbose_name_plural = 'Caminhos'

    def __str__(self):
        return self.startpointpath


class RegisteredMailDomains(models.Model):
    username = models.ForeignKey(UsersForPath, on_delete=models.CASCADE)
    domain = models.CharField(verbose_name='Domínio', max_length=100)

    class Meta:
        verbose_name = 'Domínio de e-mail'
        verbose_name_plural = 'Domínios de e-mail'

    def __str__(self):
        return self.domain + '(' + str(self.username) + ')'