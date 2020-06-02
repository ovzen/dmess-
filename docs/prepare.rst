Подготовка проекта к запуску
============================

Instructions for Ubuntu 18.04.

1. Install necessary packages

.. code-block:: bash

    sudo apt update
    sudo apt install -y build-essential make
    sudo apt install -y git
    sudo apt install -y python3 python3-venv

2. Clone the project

.. code-block:: bash

    git clone https://gitlab.informatics.ru/2019-2020/online/s101/group-04/dmess.git

3. Set up virtualenv and packages inside it

.. code-block:: bash

    cd dmess
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install -r ci/pylint_requirements.txt
    pip install -r ci/docs_requirements.txt

4. Set up Django

.. code-block:: bash

    python manage.py migrate
    python manage.py createsuperuser --username vasya --email 1@abc.net   # password: promprog
    python manage.py collectstatic

5. Create documentation.

.. code-block:: bash

    cd docs
    make html

6. Deactivate virtualenv, it is not necessary anymore.

.. code-block:: bash

    deactivate

7. Install docker.

.. code-block:: bash

    sudo apt install apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
    sudo apt update
    sudo apt install docker-ce
    sudo usermod -aG docker ${USER}    # Relogin after this command

8. Install node.js and npm

.. code-block:: bash

    curl -sL https://deb.nodesource.com/setup_13.x | sudo -E bash -
    sudo apt-get install -y nodejs
    curl -L https://npmjs.org/install.sh | sudo sh

9. Install necessary packages for frontend.
There are two parts in frontend - User and Admin, so you need to dublicade the command in two folders: fronetnd and frontend/Admin.
.. code-block:: bash

    cd frontend   # User's frontend
    npm install
