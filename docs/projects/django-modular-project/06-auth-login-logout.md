# 📘 **Django – Guide 6: Authentication (Login & Logout)**

This guide explains how to **add user authentication** (login + logout) to your Django project.
You will build a simple login form, protect pages using the `@login_required` decorator, and enable logout functionality.

> **📌 Note:**
>The repository includes a **sample SQLite database (`db.sqlite3`)** with preloaded tables and test data.

Available login credentials:

* **User account:** `user` / `demo`
* **Admin account:** `admin` / `root`

By the end of this guide, you will be able to:

* ✅ Create a **users app** for handling login + logout
* ✅ Add URL routes for `/users/login/` and `/users/logout/`
* ✅ Implement `login_view` and `logout_view`
* ✅ Create a Bootstrap login page
* ✅ Add authentication links to the global footer
* ✅ Protect pages using `@login_required`
* ✅ Redirect users after login/logout
* ✅ Make everything work using your SQLite setup

---

# 📁 **Project Structure**

```
project_folder/
├── manage.py
│
├── core/
│   ├── settings.py
│   └── urls.py
│
├── apps/
│   ├── users/
│   │   ├── apps.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── templates/users/login.html
│   │
│   ├── uom/
│   │   ├── views.py   ← protected with @login_required
│   │   └── ...
│   │
│   └── <other-apps>/
│
├── templates/
│   └── base.html       ← login/logout links in footer
│
└── db.sqlite3
```

---

# ⚙️ **1. Add Authentication Settings in `core/settings.py`**

These settings control where to redirect after login and logout:

```python
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/users/login/'
```

Also ensure your `INSTALLED_APPS` includes:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'apps.users',     # <-- our Authentication app
    'apps.uom',
    'apps.categories',
    'apps.doctype',
    'apps.items',
    'apps.compute',
]
```

---

# 🔗 **2. Add User Routes in `core/urls.py`**

```python
urlpatterns = [
    path('', include('apps.uom.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('categories/', include('apps.categories.urls')),
    path('doctype/', include('apps.doctype.urls')),
    path('items/', include('apps.items.urls')),
    path('compute/', include('apps.compute.urls')),
]
```

---

# 🧩 **3. Create the `users` App Configuration**

`apps/users/apps.py`:

```python
from django.apps import AppConfig

class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
```

---

# 🌐 **4. Create Authentication URLs**

`apps/users/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
```

---

# 🧠 **5. Create Authentication Views**

`apps/users/views.py`:

```python
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')  # Home page
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
```

---

# 🎨 **6. Create the Login Page Template**

`apps/users/templates/users/login.html`:

```html
{% extends 'base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="card shadow-lg p-4 mb-3" style="max-width: 450px; margin: 0 auto;">

    <h4 class="mb-4 text-center">Login</h4>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-danger py-2">{{ message }}</div>
        {% endfor %}
    {% endif %}

    <form method="POST">
        {% csrf_token %}

        <div class="mb-3">
            <label class="form-label">Username</label>
            <input type="text" name="username" class="form-control" required autofocus>
        </div>

        <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" name="password" class="form-control" required>
        </div>

        <button type="submit" class="btn btn-primary w-100">Login</button>
    </form>

</div>
{% endblock %}
```

---

# 🦶 **7. Add Login / Logout Links in the Footer**

`templates/base.html`:

```html
{% if user.is_authenticated %}
    <a class="ln" href="{% url 'logout' %}">「ろぐあうと」</a>
{% else %}
    <a class="ln" href="{% url 'login' %}">「ろぐいん」</a>
{% endif %}
```

Users instantly see login/logout options anywhere in the project.

---

# 🔐 **8. Protect Pages Using `@login_required`**

Example (`apps/uom/views.py`):

```python
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    ...
```

Any user who isn’t logged in is automatically redirected to:

```
/users/login/?next=/requested/page/
```

---

# 🧪 **9. Test the Full Authentication Flow**

### 1️⃣ Visit:

```
http://localhost:8000/users/login/
```

### 2️⃣ Enter a valid Django admin user

(you can create one with `python manage.py createsuperuser`)

### 3️⃣ After login → Redirects to `/`

### 4️⃣ Logout from the footer

Everything should work exactly like Guide 5 with the same clarity and flow.

---

# 🎉 **Done! Authentication is Fully Working**

You now have:

* ✔ Login page with Bootstrap
* ✔ Logout functionality
* ✔ Redirects after login/logout
* ✔ Footer showing login/logout options
* ✔ Protected views using `@login_required`
* ✔ Smooth integration with your current project
* ✔ No migrations needed — purely Django built-in auth


