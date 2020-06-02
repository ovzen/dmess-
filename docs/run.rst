Server start (developer server)
=======================================


1. Start redis

.. code-block:: bash

    docker run -p 6379:6379 -d --restart always redis:2.8

2. Activate virtualvenv

.. code-block:: bash

    source venv/bin/activate

3. Start django-сервер (in different terminal)

.. code-block:: bash

    python manage.py runserver

4. Start celery (in different terminal)

.. code-block:: bash

    export GITLAB_PRIVATE_TOKEN=<private_token>
    celery worker -B -A dmess --loglevel=debug --concurrency=4

5. Start vue-cli for User frontend (in different terminal)

.. code-block:: bash

    cd frontend          # path from the main project folder
    npm run serve

6. Start vue-cli for Admin frontend (in different terminal)

.. code-block:: bash

    cd frontend/Admin    # path from the main project folder
    npm run serve
