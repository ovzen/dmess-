# Проект "Digital messages"

### Цель
Предоставить пользователю сервис, на котором можно быстро отправить собеседнику сообщение

### Технологический стек:
- python 3.6
- django 3.0+
- sqlite 3.22+

### Инструкция по настройке проекта:
1. Склонировать проект
2. Открыть проект в PyCharm с наcтройками по умолчанию
3. Создать виртуальное окружение (через settings -> project "simple votings" -> project interpreter)
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
8. Создать конфигурацию запуска в PyCharm (файл `manage.py`, опция `runserver`)
9. Установить npm
10. Установить vue (Не точно что именно так)
```bash
npm install -g @vue/cli
npm install --save-dev webpack-bundle-tracker
npm install jsonwebtoken
```
