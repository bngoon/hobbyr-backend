# hobbyr API

<img src="https://raw.githubusercontent.com/erichowington/hobbyr/2612f880161a230048148715e7771318178134cc/public/images/hobbyr-logos/hobbyr-api.png" width="500" height="auto">

hobbyr API is a restful interface that is based on the principles of REST, which emphasize a stateless client-server interaction where resources are uniquely identified by URIs.
hobbyr is an app where users can share and interact with one another through project based posts.

## Installation

Download the API by forking and cloning this repository.

```bash
~ git clone (github url)
~ cd into directory
```

This API requires psql to interact with the database.
Enter your virtual enviorment.

```bash
~ pipenv shell
```

and install all dependencies located in the pipfile.

```bash
(hobbyr-backend) ~ pipenv install
```

A sql file that renders the databse has already been made. Run the following line command to drop the database.

```bash
(hobbyr-backend)~ psql -f create-db.sql
```

Edit the settings.py file to include the database configuration for psql and update information so that it matches yours.

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'name',
        'USER': 'user',
        'PASSWORD': 'password'
    }
}
```

Because this is made with django, their is a built in admin panel, to set it up all you do is:

```bash
(hobbyr-backend)~ python manage.py createsuperuser
```

And then,
run server.

```bash
(hobbyr-backend)~ python manage.py runserver
```

## ERD

<img src="https://raw.githubusercontent.com/erichowington/hobbyr/2612f880161a230048148715e7771318178134cc/public/images/information-systems/HOBBYR%20ERD%20(1).png" width="900" height="auto">

## API Reference

#### Register to get token

```http
  POST https://hobbyr-db-fe2543498be7.herokuapp.com/users/register/
```

body required

```bash
{
    "username" : "username",
    "email" : "email" ,
    "password" : "password"
}
```

copy "access" token and added it to Headers in **Postman**
| Key | Value | Description |
| :-------- | :------- | :-------------------------------- |
| Authorization | Bearer "acces token" | **Required**. |

### Routes

**GET** all Projects

```http
GET https://hobbyr-db-fe2543498be7.herokuapp.com/projects/
```

**GET** one project.

```http
GET https://hobbyr-db-fe2543498be7.herokuapp.com/projects/PROJECT ID
```

**CREATE** a new project

```http
POST https://hobbyr-db-fe2543498be7.herokuapp.com/projects/
```

**BODY REQUIRED**

```bash
{
    "project_title": "HOBBY",
    "project_type": "A",
    "project_img": "STRING TO IMAGE ADDRESS",
    "body": "I MADE THIS PROJECT. ITS MY HOBBY",
    "link": " ADDITIONAL LINK TO MAYBE YOUR STORE OR YOUTUBE CHANEL"
}
```

**UPDATE** your project.

```http
PUT https://hobbyr-db-fe2543498be7.herokuapp.com/projects/ PROJECT ID
```

Value you wish to update. Body required.

```bash
{
    "body": "I MADE THIS PROJECT. ITS MY PASSION",
}
```

and finally, **DELETE** Your project.

```http
DELETE https://hobbyr-db-fe2543498be7.herokuapp.com/projects/ PROJECT ID
```

## Features

- JWT Token encryption
- Virtual admin panel
- RESTful framework
- Full CRUD routes

## Tech Stack

**DATABASE:**

- Django
  **Language:**
- Python
  **RDBMS**
- PostgreSQL
  **ADDTIONAL DEPENDENCIES**
- psycopg2-binary
- djangorestframework
- django-cors-headers
- djangorestframework-simplejwt
- django-environ
- dj-database-url
- django-heroku
- whitenoise
- gunicorn

## Authors

- [@Alex Chkhikvishvili](https://www.github.com/AleksandreChkhikvishvili)
- [@Booker Ngoon](https://www.github.com/bngoon)
- [@Shatlyk](https://www.github.com/Shatlykch)
- [@Kevin Butler](https://www.github.com/kevinjbutler1994)
- [@Eric](https://www.github.com/erichowington)
