# Django App Setup: `dbpilot` with `uom` and `base.html`

## Project Structure

```
project_folder/
├── manage.py                  # Django management entrypoint
│
├── core/
│   ├── settings.py            # Centralized settings (DB, paths, debug, apps)
│   └── urls.py                # Root URL router, includes app URLs
│
├── apps/
│   └── uom/
│       ├── urls.py            # App-specific routes
│       ├── views.py           # Views / controllers
│       ├── models.py          # Database models for CRUD
│       ├── forms.py           # Forms for CRUD (optional)
│       └── templates/
│           └── uom/
│               └── index.html # App-level template
│
├── templates/
│   └── base.html              # Global base layout
│
└── static/
    ├── css/
    │   └── style.css          # Global CSS
    └── img/
        └── favicon.png         # Global images
```

## Install and setup Django, debug toolbar, folders, files

```
$ cd /home/user/Public/web
$ mkdir <project-folder>
$ cd <project-folder>
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install Django django-debug-toolbar
(venv) $ django-admin startproject core .
(venv) $ mkdir apps
(venv) $ python manage.py startapp uom
(venv) $ mv uom apps
(venv) $ mkdir templates static
(venv) $ touch templates/base.html
(venv) $ mkdir static/css
(venv) $ touch static/css/style.css
(venv) $ mkdir apps/uom/templates
(venv) $ mkdir apps/uom/templates/uom
(venv) $ touch apps/uom/templates/uom/index.html
```

## 1. `core/urls.py` — Root URL Routing

```python
# core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # For DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.uom.urls')),  # Home app
]

# Debug Toolbar URLs only if DEBUG=True
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
```

**Note:**

* `uom` is currently set as the **temporary home URL**.
* The **Django Debug Toolbar** is added for debugging. If it is not installed or configured, you can refer to the setup in the **previous guide/project** for instructions.

---

## 2. `apps/uom/urls.py` — App-specific Routes

```python
from django.urls import path
from . import views

app_name = 'uom'

urlpatterns = [
    path('', views.index, name='index'),  # Home page for the app
]
```

---

## 3. `apps/uom/views.py` — Views / Controllers

```python
from django.shortcuts import render

# Home page view
def index(request):
    context = {
        'title': 'UOM Home',  # Example context variable
        'welcome_message': 'Welcome to the UOM App!',
    }
    return render(request, 'uom/index.html', context)
```

---

## 4. `apps/uom/apps.py`

```python
from django.apps import AppConfig

class UomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.uom'   # <-- must match with `core/settings.py`
```

---

## 5. Using `base.html` in `uom/index.html`

In your `uom/templates/uom/index.html`:

```html
{% extends 'base.html' %}

{% block title %}{{title}} - Django & SQLite{% endblock %}

{% block content %}
	<div class="card shadow-lg p-4 mb-3">
    <h4 class="mb-4 text-center">Database db.sqlite3</h4>
    <div class="mb-3 d-flex flex-wrap align-items-center gap-2">
      <label for="tableSelect" class="form-label mb-0">Table:</label>
      <select class="form-select form-select-sm" id="tableSelect" style="width: auto; min-width: 150px;">
        <option value="stock_items_uom">stock_items_uom</option>			
      </select>
    </div>
  </div>
<div class="card shadow-lg p-4 mb-3">
<pre><code>CREATE TABLE "stock_items_uom" (
  "id"	INTEGER,
  "name"	TEXT NOT NULL UNIQUE,
  "description"	TEXT,
  "status"	INTEGER DEFAULT 1,
  "created_at"	DATETIME DEFAULT CURRENT_TIMESTAMP,
  "updated_at"	DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY("id" AUTOINCREMENT)
);</code></pre>

<h3>{{ title }}</h3>
<p>
{{ welcome_message }}.
This guide does not require creating a new database file. The SQLite database is already provided in the repository
along with sample data. This guide is only for displaying the schema and reading data.
</p>
 </div>
{% endblock %}
```

> `content` block must exist in `base.html` as the placeholder for page content.

---

## 6. `templates/base.html` — Global Layout

Example skeleton:

```html
<!DOCTYPE html>
<html lang="en">
<head>{% load static %}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}Django & SQLite{% endblock %}</title>
  <link href="{% static 'img/favicon.png' %}" rel="icon" type="image/x-icon">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="{% static 'css/style.css' %}" rel="stylesheet">
</head>
<body class="bg-light d-flex flex-column align-items-center">
<header><h1>Django DB Pilot Header</h1></header>
<main>
{% block content %}{% endblock %}
</main>
<footer class="attribution mt-auto py-3 bg-light text-center">
	<p>
		Template by <a href="https://getbootstrap.com/" target="_blank">Bootstrap</a>.
		Favicon by <a href="https://www.freepik.com/" target="_blank">Freepik</a>.
		Powered by <a href="https://www.djangoproject.com/" target="_blank">Django Web Framework</a>.
	</p>
</footer>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

---
## 7. Settings Reminder (`core/settings.py`)

Ensure:

```python
SECRET_KEY = 'Put-your-own-secret-key-here-!j08aqmj1dul*x5&(j$ltap'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INTERNAL_IPS = [
    "127.0.0.1",  # Localhost
    "localhost",  # Also allow localhost by name
]

INSTALLED_APPS = [
    # Default Django apps...
    'django.contrib.staticfiles',
    
    # Your apps
    'apps.uom',             # <-- must match with `apps/uom/apps.py`
    'debug_toolbar',		# <-- Debug Toolbar
] 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Global templates
        'APP_DIRS': True,                  # Looks inside app templates
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # <-- Debug Toolbar		
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

---

## ✅ 8. How it Works

1. Root URL (`''`) routes to `apps.uom.views.index`.
2. `index` view passes context variables to `uom/index.html`.
3. `index.html` extends `base.html`, injecting content into `{% block content %}`.
4. Global CSS and assets are loaded via `STATICFILES_DIRS`.

---

This is the **minimal working setup** for templating with `base.html` and using `uom` as the home app. This guide does not require creating a new database file. The SQLite database is already provided in the repository along with sample data.



