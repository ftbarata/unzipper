from django.contrib.auth import authenticate, login, logout
from .models import Paths, UsersForPath
import subprocess


def _login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return True
        else:
            return False
    else:
        return False


def _logout(request):
    request.session.flush()
    logout(request)
    return True


def checkPath(username,path):
    if UsersForPath.objects.filter(username=username).exists():
        queryset = Paths.objects.filter(username=UsersForPath.objects.get(username=username))
        for i in queryset:
            if i.startpointpath == path:
                return True
        return False
    else:
        return False


def checkPartidas(request):
    if UsersForPath.objects.filter(username=request.user).exists():
        partidas = Paths.objects.filter(username=UsersForPath.objects.get(username=request.user))
        if partidas:
            return partidas
        else:
            return False


def zimbraQuotaUsage(domain):
    result = subprocess.run(['ssh', '-C', 'root@mx.manancialturismo.com.br','cat /root/fellipe_zimbra_quota_usage.txt'], stdout=subprocess.PIPE)
    response = result.stdout.decode('utf-8').splitlines()
    tuples_list = []
    updated_at = ''
    for line in response:
        print(line)
        if 'Conta' not in line and 'Cota_Total' not in line:
            if '/' in line:
                updated_at = line
            else:
                if domain.lower() in line.lower():
                    if 'admin@' not in line.split()[0].lower():
                        if len(line.split()) == 5:
                            tuples_list.append((line.split()[0], line.split()[1] + ' ' + line.split()[2], line.split()[3] + ' ' + line.split()[4]))
                        elif len(line.split()) == 3:
                            tuples_list.append((line.split()[0], line.split()[1] + ' ' + line.split()[2]))
    return (sorted(tuples_list, key=lambda tup: tup[0]), updated_at)
