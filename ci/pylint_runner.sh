#!/usr/bin/env bash

cd ~/dmess/ || exit

#pylint admin/ dmess/ main/
pylint --load-plugins pylint_django -j 0 ./main
