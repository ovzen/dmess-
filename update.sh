#!/usr/bin/env bash

cd ~/dmess/ || exit

echo "Receiving updated sources"
git checkout master
git stash
git pull
git stash pop

echo "Installing dependencies"
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate

echo "Getting updated static files"
cd ~/dmess/frontend || exit
npm install
npm run build
cd ..
cp -R frontend/dist/* templates/
python manage.py collectstatic

echo "Restarting server"
sudo /bin/systemctl restart dmess_celery
sudo /bin/systemctl restart dmess_daphne
sudo /bin/systemctl restart nginx
