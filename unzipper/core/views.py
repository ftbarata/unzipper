from django.shortcuts import render, redirect
from .helper_functions import _login, _logout
from django.core.files.storage import FileSystemStorage
import rarfile, zipfile,os
from .helper_functions import checkPath


def home(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'core/home.html')
        elif request.method == 'POST':
            if request.FILES:
                file = request.FILES['file']
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                uploaded_file_url = fs.url(filename)
                if not rarfile.is_rarfile(file) or not zipfile.is_zipfile(file):
                    os.remove(os.path.join(fs.location, filename))
                    return render(request, 'core/home.html',{'error_message': 'Arquivo não é zip nem rar.'})
                else:
                    return render(request, 'core/home.html', {'status_message': 'Arquivo enviado para: {}'.format(uploaded_file_url)})
            else:
                return render(request, 'core/home.html', {'error_message': 'Nenhum arquivo foi selecionado para upload.'})
    else:
        return redirect('login')


def login(request):
    if request.method == 'POST':
        if _login(request):
            return render(request, 'core/home.html')
        else:
            context = {'error_message': 'Acesso negado. Verifique seu login e senha.'}
            return render(request, 'core/login.html', context)
    else:
        return render(request, 'core/login.html')


def logout(request):
    _logout(request)
    return render(request,'core/login.html', {'status_message':'Você foi deslogado.'})


def checkPathView(request, path):
    if checkPath(request.user, path):
        return render(request, 'core/ajax.html', {'result':'True'})
    else:
        return render(request, 'core/ajax.html', {'result': 'False'})