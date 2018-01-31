from django.contrib.auth import authenticate, login, logout
import os
from .models import Paths, UsersForPath

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
    if UsersForPath.objects.all().filter(username=username).exists():
        queryset = Paths.objects.get(username=UsersForPath.objects.get(username=username))
        for i in queryset:
            if os.path.join(i.startpointpath, path):
                return True
        return False
    else:
        return False

