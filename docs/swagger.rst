Setting up Swagger
=============================

Installing swagger
-----------------

1. Install swagger:

pip install django-rest-swagger

2. Change line `{% load staticfiles %}` to `{% load static %}` in file index.html :

    /venv/lib/python3.6/site-packages/rest_framework_swagger/templates/rest_framework_swagger/

3. Docs  `http://127.0.0.1:8000/docs/`

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
