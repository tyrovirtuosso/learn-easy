# learn-easy
Learn anything, easily with a supercharged Anki, that incorporates GPT flawlessly!

To run:
uvicorn learn_easy.asgi:application --port 8000 --workers 4 --log-level debug --reload
or
python manage.py runserver

# Commonly Used for setup
python manage.py makemigrations cards dashboard decks usersApp
python manage.py makemigrations
python manage.py migrate
python manage.py runserver      
python manage.py collectstatic
python manage.py shell
python manage.py reset_db
python manage.py runscript query -v2
redis-server
celery -A learn_easy worker --loglevel=info
celery -A learn_easy beat -l info
npm install -D tailwindcss
npx tailwind
npx tailwindcss init
