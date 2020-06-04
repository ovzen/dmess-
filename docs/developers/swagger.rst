Установка и настройка swagger
=============================

Установка swagger
-----------------

1. Установить swagger (необязательно, если requirements.txt установлены):

pip install django-rest-swagger

2. Изменить в файле index.html по пути:

    /venv/lib/python3.6/site-packages/rest_framework_swagger/templates/rest_framework_swagger/

    Строчку `{% load staticfiles %}` На `{% load static %}`
3. После запуска серверов документация доступна по адресу `http://127.0.0.1:8000/docs/`

Описание API функции
--------------------
1. Убедиться, что у этой функции прописан path
2. В views функции в самом начале прописать описание и, если необходимо, параметры (они обычно находятся автоматически)

.. code-block:: json

    """
        Registration of new user
        param1 -- A first parameter
        param2 -- A second parameter
    """
