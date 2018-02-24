from django.shortcuts import render, redirect
from .helper_functions import _login, _logout
from django.core.files.storage import FileSystemStorage
import rarfile, zipfile,os
from .helper_functions import checkPath, checkPartidas, zimbraQuotaUsage
from django.views.decorators.csrf import csrf_exempt
from .models import Paths, UsersForPath, RegisteredMailDomains
from django.conf import settings
import os, subprocess


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
    if request.user.is_authenticated:
        if UsersForPath.objects.filter(username=request.user).exists():
            can_change_password = UsersForPath.objects.get(username=request.user).can_change_password
            if RegisteredMailDomains.objects.all().filter(username=UsersForPath.objects.get(username=request.user)).exists():
                registered_mail_domains = RegisteredMailDomains.objects.all().filter(username=UsersForPath.objects.get(username=request.user))
                mails = []
                updated_at = ''
                for i in registered_mail_domains:
                    domain_mails_tuple_list = (i.domain, zimbraQuotaUsage(i.domain)[0])
                    mails.append(domain_mails_tuple_list)
                    updated_at = zimbraQuotaUsage(i.domain)[1]
                return render(request, 'core/emails.html', {'mails': mails, 'updated_at': updated_at, 'can_change_password': can_change_password})
            else:
                return render(request, 'core/emails.html')
        else:
            return render(request, 'core/emails.html')
    else:
        return redirect('login')


def changeMailPassword(request, email):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'core/change_mail_password.html', {'email': email})
        else:
            return render(request, 'core/change_mail_password.html', {'error_message': 'Método não foi GET.'})
    else:
        return redirect('login')


def changeMailPasswordFromForm(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST['password']:
                email = request.POST['email']
                new_password = request.POST['password']
                result = subprocess.run(['ssh', '-C', 'root@mx.manancialturismo.com.br', 'su - zimbra -c "zmprov sp {} {}"'.format(email,new_password)],stdout=subprocess.PIPE)
                response = result.stdout.decode('utf-8')
                if len(response) == 0:
                    return render(request, 'core/change_mail_password.html', {'status_message':'Senha alterada com sucesso.', 'email': email})
                else:
                    return render(request, 'core/change_mail_password.html',{'error_message': 'Ocorreu um erro na operação. Contacte o suporte.', 'email': email})
            else:
                return render(request, 'core/change_mail_password.html',{'error_message': 'Senha não informada.'})
        else:
            return render(request, 'core/change_mail_password.html', {'error_message': 'Método não foi POST.'})
    else:
        return redirect('login')
