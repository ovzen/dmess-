###Установка swagger

1. Установить swagger:    
    ```bash
    pip install django-rest-swagger
    ```
2. Изменить в файле index.html по пути:
    ```
    /venv/lib/python3.6/site-packages/rest_framework_swagger/templates/rest_framework_swagger/
    ```
    Строчку ```{% load staticfiles %}``` На ```{% load static %}```
3. После запуска серверов документация доступна по адресу ```http://127.0.0.1:8000/docs/```