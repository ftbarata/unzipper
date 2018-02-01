from django.shortcuts import render, redirect
from .helper_functions import _login, _logout
from django.core.files.storage import FileSystemStorage
import rarfile, zipfile,os
from .helper_functions import checkPath
from django.views.decorators.csrf import csrf_exempt
from .models import Paths, UsersForPath


def home(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            if UsersForPath.objects.filter(username=request.user).exists():
                partidas = Paths.objects.filter(username=UsersForPath.objects.get(username=request.user))
                if partidas:
                    return render(request, 'core/home.html', {'partidas':partidas})
                else:
                    return render(request, 'core/home.html', {'msg': 'Nenhum ponto de partida autorizado.'})
        elif request.method == 'POST':
            print(request.POST)
            if request.FILES:
                file = request.FILES['file']
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                # uploaded_file_url = fs.url(filename)
                if not rarfile.is_rarfile(file) and not zipfile.is_zipfile(file):
                    os.remove(os.path.join(fs.location, filename))
                    return render(request, 'core/home.html',{'error_message': 'Arquivo não é zip nem rar.'})
                else:
                    startpoint = request.POST['path']
                    abs_path_to_uploaded_file = os.path.join(fs.location, filename)
                    if 'pathleft' in request.POST:
                        pathleft = request.POST['pathleft']
                        if not os.path.isdir(os.path.join(startpoint,pathleft)):
                            return render(request, 'core/home.html', {'error_message': 'O caminho informado não existe.'})
                        else:
                            os.system('cp -f {} {}'.format(abs_path_to_uploaded_file, os.path.join(startpoint, pathleft)))
                            os.chdir(os.path.join(startpoint, pathleft))
                            if rarfile.is_rarfile(file):
                                os.system('unrar {}'.format(filename))
                            elif zipfile.is_zipfile(file):
                                os.system('unzip {}'.format(filename))
                            os.system('rm -f {}'.format(filename))
                            os.remove(abs_path_to_uploaded_file)

                        return render(request, 'core/home.html',{'status_message': 'Descompactação executada com sucesso'})

                    else:
                        if not os.path.isdir(startpoint):
                            return render(request, 'core/home.html', {'error_message': 'O caminho informado não existe.'})
                        else:
                            os.system('cp -f {} {}'.format(abs_path_to_uploaded_file, startpoint))
                            os.chdir(startpoint)
                            if rarfile.is_rarfile(file):
                                os.system('unrar {}'.format(filename))
                            elif zipfile.is_zipfile(file):
                                os.system('unzip {}'.format(filename))
                            os.system('rm -f {}'.format(filename))
                            os.remove(abs_path_to_uploaded_file)

                        return render(request, 'core/home.html',{'status_message': 'Descompactação executada com sucesso'})
            else:
                return render(request, 'core/home.html', {'error_message': 'Nenhum arquivo foi selecionado para upload.'})
    else:
        return redirect('login')


def login(request):
    if request.method == 'POST':
        if _login(request):
            if UsersForPath.objects.filter(username=request.user).exists():
                partidas = Paths.objects.filter(username=UsersForPath.objects.get(username=request.user))
                if partidas:
                    return render(request, 'core/home.html', {'partidas':partidas})
                else:
                    return render(request, 'core/home.html', {'msg': 'Nenhum ponto de partida autorizado.'})
        else:
            context = {'error_message': 'Acesso negado. Verifique seu login e senha.'}
            return render(request, 'core/login.html', context)
    else:
        return render(request, 'core/login.html')


def logout(request):
    _logout(request)
    return render(request,'core/login.html', {'status_message':'Você foi deslogado.'})


@csrf_exempt
def checkPathView(request):
    if request.method == 'POST':
        path = request.POST['inputpath']
        if checkPath(request.user, path):
            return render(request, 'core/ajax.html', {'result':'True'})
        else:
            return render(request, 'core/ajax.html', {'result': 'False'})
    else:
        return render(request, 'core/ajax.html', {'result': 'GET METHOD'})