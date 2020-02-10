# Проект "Digital messages"

### Цель
Предоставить пользователю сервис для обмена мгновенными сообщениями

### Технологический стек:
- python 3.6
- django 3.0+
- sqlite 3.22+
- djangorestframework
- channels
- redis
- vue 

### Инструкция по настройке проекта:
1. Склонировать проект
2. Открыть проект в PyCharm с наcтройками по умолчанию
3. Создать виртуальное окружение (через settings -> project "dmess" -> project interpreter)
4. Открыть терминал в PyCharm, проверить, что виртуальное окружение активировано.
5. Обновить pip:
    ```bash
    pip install --upgrade pip
    ```
6. Установить в виртуальное окружение необходимые пакеты: 
    ```bash
    pip install -r requirements.txt
    ```
7. Синхронизировать структуру базы данных с моделями: 
    ```bash
    python manage.py migrate
    ```
8. Собрать static файлы командой
    ```bash
    python manage.py collectstatic
    ```

9. Создать конфигурацию запуска в PyCharm (файл `manage.py`, опция `runserver`)

10. Установить docker
    ```bash 
    apt install docker.io
    ```
11. Создать группу докер
    ```bash 
    sudo groupadd docker
    ```
12. Добавить своего пользователя в эту группу 
    ```bash 
    sudo usermod -aG docker $USER
    ```
    Где вместо "$USER" ваш пользователь, например "prom"
13. Перезагрузить машину
14. Для проверки работоспособности докера выполнить:
    ```bash 
    docker run hello-world
    ```
    Если ошибок нет,  т.е. произошла загрузка и вывод тестового сообщения в консоль, значит всё ок.
15. Запустить redis: 
    ```bash 
    docker run -p 6379:6379 -d redis:2.8
    ```
16. Скачать и установить npm
    ```bash 
        sudo apt install npm
    ```
17. В папке фронтенд выполнить команду ```npm install```. Выполнение займет какое-то время.

При запуске сервера в папке фронтенд выполнить команду ```npm run serve```.
А после запускать сервер Django.