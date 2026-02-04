# Rest API

is a way for two systems – like a website and a server – to talk to each other using standard HTTP methods like GET, POST, PUT, and DELETE.

> in a ToDo app
> 
> 1. Get list of tasks
> 2. Add a new task
> 3. Update a task 
> 4. Delete a task
>

## Tools Needed to develop REST API

- Python (preferably 3.8+)
- Django (web framework)
```shell
pip install django
```
- Django REST Framework (DRF) (to build APIs)
```shell
pip install djangorestframework
```
- Postman or curl (for testing)

## Steps Taken

### 1. Set up project 

```shell
django-admin startproject [project name] . # Creates a new Django project 
python3 manage.py startapp api # Creates a new Django app called api
```

add the `rest_framework` and `api` to the `INSTALLED_APPS`

```python
# settings.py 
INSTALLED_APPS = [
    ...
    'rest_framework', # Django REST Framework – it gives you tools to easily create APIs.
    'api', # tells Django to look in the api folder for models, views, and so on.
]
```

### 2. Create a model

```

