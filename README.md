python3 -m venv venv
source venv/bin/activate

pip install django
pip install pillow

django-admin startproject core .

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runserver