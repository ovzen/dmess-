import datetime

from django.shortcuts import render


def get_base_context():
    context = {
        'menu': [
            {'link': '/', 'text': 'Главная'},
            {'link': '/admin', 'text': 'Админ-панель'},
        ],
        'current_time': datetime.datetime.now(),
        'title': 'untitled',
    }
    return context


def index_chat(request):
    context = get_base_context()
    context['title'] = 'Главная страница - dmess'
    context['main_header'] = 'Digital Messages'
    return render(request, 'chat/index.html', context)


def index_page(request):
    context = get_base_context()
    # context['title'] = 'Основной чат'
    context['main_header'] = 'Digital Messages'
    return render(request, 'index.html', context)
