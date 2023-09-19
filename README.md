# learn-easy
Learn anything, easily with a supercharged Anki, that incorporates GPT flawlessly!

To run:
uvicorn learn_easy.asgi:application --port 8000 --workers 4 --log-level debug --reload
or
python manage.py runserver

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py shell
