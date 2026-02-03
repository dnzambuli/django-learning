# some highly recommended titles:

1. **"Django for Beginners" by William S. Vincent**  
   This book is great for those who are new to Django. It provides a hands-on approach with practical projects to help you understand the framework.

2. **"Django for Professionals" by William S. Vincent**  
   Building on "Django for Beginners," this book is aimed at those who already have a basic understanding of Django and want to build more advanced applications. It covers topics such as deployment, authentication, and more.

3. **"Two Scoops of Django" by Audrey Roy Greenfeld and Daniel Roy Greenfeld**  
   This book is suitable for developers who have some experience with Django. It offers best practices, tips, and techniques for writing efficient Django code and building maintainable applications.

4. **"Django 3 By Example" by Antonio Melé**  
   This book teaches Django by guiding you through the development of several projects, helping you learn through practical application.

5. **"Django Unleashed" by Andrew Pinkham**  
   A comprehensive guide for those looking to understand Django in depth. It covers a wide variety of topics and includes practical examples and thorough explanations.

6. **"Build a Backend REST API with Python & Django" by Mark Winterbottom**  
   This book focuses specifically on building RESTful APIs with Django, a valuable skill if you're interested in backend development.

> **Point to Note**
>
> When choosing a book, consider your current knowledge of Python and web development, as well as your learning style, to find the best fit for you. Additionally, supplementing your learning with online resources, tutorials, and official documentation can provide a well-rounded understanding of Django.

---

# Django

1. Creating a new Django project called test_project

```bash
(django) $ django-admin startproject test_project .
```

The `.` tells django to create the project in the current directory and not make a new `test_project` folder

2. Running Django's local web server

```bash
(django) $ python manage.py runserver
```

3. Stop django local server

```bash
(django) $ [ctrl + c]
```

4. Stop virtual environment

```bash
(django) $ exit
```

5. Create an app `pages app`

```bash
(helloworld) $ python manage.py startapp pages
```

6. Register the application

> add the app to `settings.py` under `INSTALLED_APPS =[...,<APPNAME>.apps.<APPNAME>Config]

# Django File Structure

```bash
├── helloworld_project
│├── __init__.py
│├── settings.py
│├── urls.py
│└── wsgi.py
└── manage.py
```

1. **settings.py** controls our project settings
2. **urls.py** tells Django which pages to build in response to a browser or URL request
3. **wsgi.py (Web Server Gateway Interface)** helps Django serve our eventual web pages)
4. **manage.py** is used to execute various Django commands such as running the local web
   server or creating a new app

# Apps

Django uses the concept of projects and apps to keep code clean and readable.

A single Django project contains one or more apps within it that all work together to power a
web application.

> For example, a real-world Django e-commerce site might have:
>
> - one app for user authentication,
> - another app for payments, and
> - a third app to power item listing details
>
> each focuses on an isolated piece of functionality _three distinct apps that all live within one top-level project_.

## App File Structure

```bash
├── pages
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
```

- **admin.py** is a configuration file for the built-in Django Admin app
- **apps.py** is a configuration file for the app itself
- **migrations/** keeps track of any changes to our models.py file so our database and models.py stay in sync
- **models.py** is where we define our database models which Django automatically translates into database tables
- **tests.py** is for our app-specific tests
- **views.py** is where we handle the request/response logic for our web app

## Install APPs

Django doesn’t “know" about an app until we explicitly add it.

---

# URLs, Views, Models, Templates

From typing in a URL, such as https://djangoforbeginners.com,

1. the first thing that happens within our Django project is a `URLpattern` is found that matches the homepage.
2. The URLpattern specifies `a view` which
3. then determines the content for the page (usually from a database `model`) and
4. then ultimately `a template `for styling and basic logic.

The end result is sent back to the user as an `HTTP response`.

```
URL -> View -> Model (typically) -> Template
```

> Django **views** determine what content is displayed on a given page while **URLConfs** determine where that content is going. The **model** contains the content from the database and the **template** provides styling for it.
