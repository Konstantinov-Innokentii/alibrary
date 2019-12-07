Alibrary
=============================

Alibrary is simple REST server for library, written using Django 2 and Django Rest Framework

## INSTALLATION

After cloning the repo, add file  **`.env.dev`** to the root of project:

    SECRET_KEY=MySecretKey
    DEBUG=True
    SQL_ENGINE=django.db.backends.postgresql
    SQL_DATABASE=MyDatabase
    SQL_USER=MyUser
    SQL_PASSWORD=MyPassword
    SQL_HOST=db
    SQL_PORT=5432

**Change** **`SECRET_KEY`** and DB credentials

**Note** that if you set:

    DEBUG=False
    
you have to provide

    ALLOWED_HOSTS 

## Running

Run docker container with:

    docker-compose up -d --build

**Don't forget** to apply migrations at first startup and create superuser **after** this:

    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    
## Usage

You cand find list of api methods at **`/swagger-docs`**

1.There you can test not only session Authentication, but also JWT auth token. To do this click on the Authorize and insert as a value:
      
      Bearer yourAccessToken

  You can get acess token at **api/v1/token** endpoint inside swagger-docs, or with curl:

  (For example you can use superuser credentials)
    
      curl \
      -X POST \
      -H "Content-Type: application/json" \
      -d '{"username": "username, "password": "password"}' \
      http://localhost:8000/api/v1/token/
    
2. Also note, that to assign book to a reader you have to send **only** reader id, not object.    


    
 
