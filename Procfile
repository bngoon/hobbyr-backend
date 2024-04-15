
# The migrate command is to migrate the app models/ tables to the database hosted in heroku servers.
release: python3 manage.py migrate

# gunicorn will allow us to deploy to heroku 
# It will act as a middleman between our application and the internet.
web: gunicorn hobbyr_backend.wsgi 
