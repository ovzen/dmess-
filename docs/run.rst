Запуск сервера (вариант для разработки)
=======================================


1. Запустить redis

.. code-block:: bash

    docker run -p 6379:6379 -d redis:2.8

2. Активировать виртуальное окружение

.. code-block:: bash

    source venv/bin/activate

3. Запустить django-сервер (в отдельном терминале)

.. code-block:: bash

    python manage.py runserver

4. Запустить celery (в отдельном терминале)

.. code-block:: bash

    export GITLAB_PRIVATE_TOKEN=<private_token>
    celery worker -B -A dmess --loglevel=debug --concurrency=4

5. Запустить vue-cli для клиентского фронтенда (в отдельном терминале)

.. code-block:: bash

    cd frontend          # указан путь от корневой папки проекта
    npm run serve

6. Запустить vue-cli для админского фронтенда (в отдельном терминале)

.. code-block:: bash

    cd frontend/Admin    # указан путь от корневой папки проекта
    npm run serve
