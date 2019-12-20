import datetime

from django.shortcuts import render


def get_base_context():
    context = {
        'menu': [
            {'link': '/', 'text': 'Главная'},
            {'link': '/dialogs', 'text': 'Диалоги'},
            {'link': '/about', 'text': 'Информация'},
            {'link': '/admin', 'text': 'Админ-панель'},
        ],
        'title': 'untitled',
    }
    return context


def index_page(request):
    context = get_base_context()
    context['title'] = 'Главная страница - Dmess'
    context['main_header'] = 'Digital Messages'
    return render(request, 'index.html', context)

def dialog_page(request):
    context = get_base_context()
    context['title'] = 'Диалоги - Dmess'
    context['main_header'] = 'Диалоги'
    # Код диалога
    if False:  # Заглушка

        context['not_auth'] = False
    else:
        context['not_auth'] = True
        context['error'] = 'Вы не авторизованы!'
    return render(request, 'dialogs.html', context)

def about_page(request):
    context = get_base_context()
    context['title'] = 'Информация - Dmess'
    context['main_header'] = 'Информация'
    return render(request, 'about.html', context)