#!/usr/bin/env bash

coverage run --omit venv manage.py test
coverage report --omit=manage.py
coverage html --omit=manage.py
mkdir public
mv htmlcov public/coverage
