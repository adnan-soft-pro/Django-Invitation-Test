# Overview

This is a test task based on django + django-rest-framework to find real talented programmer.

# Quick start

  - Install all packages from requirements.txt
```sh
   $ pip install -r requirements.txt
```
  - Migrate app, create superuser and run project.
```sh
   $ python manage.py migrate
   $ python manage.py createsuperuser
   $ python manage.py runserver
```
  - Project will run on http://127.0.0.1:8000/
  
# API Information

/ Request Method | Endpoints | Description |
| ------ | ------ | ------ |
| GET | /api/invitations/ | Show the list of Invitations |
| POST | /api/invitations/ | Create a new Invitation|
| PATCH | /api/invitations/\<id\>/ | Partial update a specific Invitation by id with body |
| DELETE | /api/invitations/\<id\>/ | Delete a specific Invitation by id |
