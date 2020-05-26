#!/bin/bash

# run pylint
pylint --load-plugins pylint_django -j 0 ./main | tee pylint.txt

# get badge
#mkdir public
score=$(sed -n 's/^Your code has been rated at \([-0-9.]*\)\/.*/\1/p' pylint.txt)
#score='lalalala'
#anybadge --value=$score --file=public/pylint.svg pylint
echo "test test test Pylint score was $score"

rm pylint.txt
exit 0