Подготовка проекта к запуску
============================

Инструкция предоставлена для Ubuntu 18.04.

1. Устанавливаем необходимые пакеты в систему

.. code-block:: bash

    sudo apt update
    sudo apt install -y build-essential make
    sudo apt install -y git
    sudo apt install -y python3 python3-venv

2. Клонируем проект

.. code-block:: bash

    git clone https://gitlab.informatics.ru/2019-2020/online/s101/group-04/dmess.git

3. Настраиваем virtualenv и пакеты в нём

.. code-block:: bash

    cd dmess
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install -r ci/pylint_requirements.txt
    pip install -r ci/docs_requirements.txt

4. Выполняем базовые действия в django

.. code-block:: bash

    python manage.py migrate
    python manage.py createsuperuser --username vasya --email 1@abc.net   # указать пароль promprog
    python manage.py collectstatic

5. Создаём документацию проекта.

.. code-block:: bash

    cd docs
    make html

6. После этого можно отключить virtualenv, для настройки он больше не понадобится

.. code-block:: bash

    deactivate

7. Устанавливаем docker

.. code-block:: bash

    sudo apt install apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
    sudo apt update
    sudo apt install docker-ce
    sudo usermod -aG docker ${USER}    # После этой команды нужно перезалогиниться

8. Устанавливаем node.js и npm в систему

.. code-block:: bash

    curl -sL https://deb.nodesource.com/setup_13.x | sudo -E bash -
    sudo apt-get install -y nodejs
    curl -L https://npmjs.org/install.sh | sudo sh

9. Устанавливаем необходимые пакеты в проекте.
Фронтенд состоит из двух частей, клиентской и админской, каждая в своей папке. Поэтому команды дублируются.

.. code-block:: bash

    cd frontend   # Здесь лежит клиентский фронтенд
    npm install
