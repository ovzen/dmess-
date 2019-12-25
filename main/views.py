import datetime

from django.shortcuts import render

from dmess.settings import BASE_ADDRESS


def get_base_context():
    context = {
        'menu': [
            {'link_name': 'index', 'text': 'Главная'},
            {'link_name': 'dialogs', 'text': 'Диалоги'},
            {'link_name': 'about', 'text': 'Информация'},
            {'link_name': 'admin:index', 'text': 'Админ-панель'},
        ],
        'index_link_name': 'index',
        'title': 'untitled',
    }
    return context


def index_page(request):
    context = get_base_context()
    context['title'] = 'Главная страница - Dmess'
    context['main_header'] = 'Digital Messages'
    return render(request, 'index.html', context)


def sitemap_page(request):
    context = get_base_context()
    context['base_address'] = BASE_ADDRESS
    return render(request, 'sitemap.xml', context)


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
