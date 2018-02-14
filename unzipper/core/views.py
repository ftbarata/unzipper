from django.shortcuts import render, redirect
from .helper_functions import _login, _logout
from django.core.files.storage import FileSystemStorage
import rarfile, zipfile,os
from .helper_functions import checkPath, checkPartidas, zimbraQuotaUsage
from django.views.decorators.csrf import csrf_exempt
from .models import Paths, UsersForPath, RegisteredMailDomains
from django.conf import settings
import os


def home(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            if checkPartidas(request):
                return render(request, 'core/home.html', {'partidas':checkPartidas(request)})
            else:
                return render(request, 'core/home.html', {'msg': 'Nenhum ponto de partida autorizado.'})
        elif request.method == 'POST':
            if checkPartidas(request):
                msg = checkPartidas(request)
            else:
                msg = 'Nenhum ponto de partida autorizado.'

            if not checkPath(request.user, request.POST['pathname']):
                return render(request, 'core/home.html',{'error_message': 'Sem permissão para o ponto de partida.', 'msg': msg, 'partidas': msg})

            if request.FILES:
                file = request.FILES['file']
                if os.path.isfile(os.path.join(settings.MEDIA_ROOT, str(file))):
                    os.remove(os.path.join(settings.MEDIA_ROOT, str(file)))
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                # uploaded_file_url = fs.url(filename)

                if not rarfile.is_rarfile(file) and not zipfile.is_zipfile(file):
                    os.remove(os.path.join(fs.location, filename))
                    return render(request, 'core/home.html',{'error_message': 'Arquivo não é zip nem rar.', 'msg': msg, 'partidas': msg})
                else:
                    startpoint = request.POST['pathname']

                    abs_path_to_uploaded_file = os.path.join(fs.location, filename)

                    if 'pathnameleft' in request.POST:
                        pathleft = request.POST['pathnameleft']
                    else:
                        return render(request, 'core/home.html',{'error_message': 'Complemento(obrigatório) do caminho não informado.', 'msg': msg, 'partidas': msg})

                    # if Paths.objects.all().filter(username=request.user).exists() and UsersForPath.objects.all().filter(username=request.user):
                    #     paths = Paths.objects.all().filter(username=UsersForPath.objects.get(username=request.user))
                    # else:
                    #     paths =

                    if not os.path.isdir(os.path.join(startpoint,pathleft)):
                        return render(request, 'core/home.html', {'error_message': 'O caminho informado não existe.', 'msg': msg, 'partidas': msg})
                    else:
                        os.system('cp -f {} {}'.format(abs_path_to_uploaded_file, os.path.join(startpoint, pathleft)))
                        os.chdir(os.path.join(startpoint, pathleft))
                        if rarfile.is_rarfile(file):
                            os.system('unrar x -o+ {}'.format(filename))
                        elif zipfile.is_zipfile(file):
                            os.system('unzip -o {}'.format(filename))
                        os.system('rm -f {}'.format(filename))
                        os.system('chown -R ftpconntrack:daemon *')
                        os.system('find . -type f -exec chmod 640 {} \;')
                        os.system('find . -type d -exec chmod 750 {} \;')
                        os.remove(abs_path_to_uploaded_file)

                    return render(request, 'core/home.html',{'error_message': 'Descompactação executada com sucesso', 'msg': msg, 'partidas': msg})
            else:
                return render(request, 'core/home.html', {'error_message': 'Nenhum arquivo foi selecionado para upload.', 'msg': msg, 'partidas': msg})
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


def emails(request):
    if UsersForPath.objects.filter(username=request.user).exists():
        if RegisteredMailDomains.objects.all().filter(username=UsersForPath.objects.get(username=request.user)).exists():
            registered_mail_domains = RegisteredMailDomains.objects.all().filter(username=UsersForPath.objects.get(username=request.user))
            mails = []
            updated_at = ''
            for i in registered_mail_domains:
                domain_mails_tuple_list = (i.domain, zimbraQuotaUsage(i.domain)[0])
                mails.append(domain_mails_tuple_list)
                updated_at = zimbraQuotaUsage(i.domain)[1]
            if updated_at:
                return render(request, 'core/emails.html', {'mails': mails, 'updated_at': updated_at})
            else:
                return render(request, 'core/emails.html', {'info_message': 'Arquivo contendo a lista de e-mails vazio ou não encontrado. Comunique ao suporte.'})
        else:
            return render(request, 'core/emails.html', {'info_message': 'Não há emails associados ao seu usuário.'})
    else:
        return render(request, 'core/emails.html', {'info_message': 'Seu usuário ainda não foi cadastrado para listar e-mails.'})
