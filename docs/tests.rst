Создание и запуск тестов для API
================================

Создание тестов
---------------
1. Открываем файл **tests.py** (расположен
в папках **admin/** и **main/** для админской
и клиентской части соответственно).

2. Используя уже написанные тесты, а также
инструкции по их написанию в документациях
django и django rest framework, пишем новые тесты.

- Тестирование (Django): https://docs.djangoproject.com/en/3.0/topics/testing/
- Тестирование (DRF): https://www.django-rest-framework.org/api-guide/testing/

Запуск тестов
-------------
1. Переходим в корневую папку проекта.
2. Запускаем тесты:

.. code-block:: bash

    python manage.py test

Установка и запуск coverage
---------------------------
1. Устанавливаем coverage (если не установлены requirements.txt):

.. code-block:: bash

    pip install coverage

2. Переходим в корневую папку проекта.

3. Запускаем тесты с измерением coverage:

.. code-block:: bash

    coverage run manage.py test

4. Выводим на экран отчёт о покрытии (исключая папку виртуального окружения):

.. code-block:: bash

    coverage report --omit=venv/*

5. Создаем интерактивную html страницу с отчетом о покрытии (исключая папку виртуального окружения):

.. code-block:: bash

    coverage html -i --omit=venv/*

После этой команды в проекте появится папка htmlcov, в которой надо открыть index.html
