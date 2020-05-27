#!/usr/bin/env bash

coverage run --omit='venv/*' manage.py test
coverage report --omit=manage.py,venv
coverage html --omit=manage.py,venv
mkdir public
mv htmlcov public/coverage
