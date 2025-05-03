pip freeze > requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py makemessages -l ar
python manage.py compilemessages
python manage.py runserver 0.0.0.0:8000
