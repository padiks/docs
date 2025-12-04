# **Guide 8 — Role-Based Django Admin (Users vs Admin Group)**

This guide explains how the Django Admin has been customized to:

* Allow **Admins** full access to users.
* Restrict **Users group** from changing passwords.
* Keep branding, logo, and favicon intact.

We only have **three working files** for this customization.

The repository includes a **sample SQLite database (`db.sqlite3`)** with preloaded tables and test data.

Available login credentials:

* **User account:** `user` / `demo`
* **Admin account:** `admin` / `root`

---

# 📁 **Project Structure**

```
project_folder/
├── manage.py
│
├── core/
│
├── apps/
│   │
│   ├── . . .
│   │ 
│   ├── users/
│   │   ├── apps.py
│   │   ├── admin.py                 # <----- Django Admin configuration
│   │   ├── urls.py
│   │   ├── views.py                 # <----- Django Admin (login/logout view)
│   │   ├── templates/users/
│   │   │    └── login.html    
│   │   └── templatetags/            # <----- Django Admin (template filter for roles)
│   │        └── group_filters.py    # <----- Django Admin
│   │
│   └── <other-modules>/
│
├── templates/
│   ├── base.html
│   ├── includes/
│   │    └── _table_select.html      
│   └── admin/
│       └── base_site.html           # <----- Django Admin custom page
│
└── db.sqlite3
```

This shows **exactly which files are involved in Role-Based Django Admin**:

* `admin.py` → custom User admin + role permissions
* `views.py` → login/logout for Django Admin
* `templatetags/group_filters.py` → template filter to detect user groups
* `templates/admin/base_site.html` → custom admin page
* `login.html` → admin login template

---

## **1️⃣ apps/users/admin.py**

**Purpose:** Customize how Django Admin displays and allows actions on the `User` table.

```python
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):

    # Show important info columns in the admin list
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')

    # Permissions based on group:
    # Admin group → full access
    # Users group → cannot view, add, change, or delete users
    def has_view_permission(self, request, obj=None):
        return request.user.groups.filter(name='Admin').exists() or request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='Admin').exists() or request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.groups.filter(name='Admin').exists() or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='Admin').exists() or request.user.is_superuser

# Remove default Django User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
```

**Key points:**

* Admin group members (or superusers) can manage users normally.
* Users in the Users group **cannot even see the User table** in Django Admin.

---

## **2️⃣ templates/admin/base_site.html**

**Purpose:** Customize the Django Admin template for:

* Branding (`Django Admin`)
* Favicon (`favicon.png`)
* Hiding the “Change password” link **only for Users group**.

```html
{% extends "admin/base.html" %}
{% load group_filters %}
{% load static %}

{% block title %}Django Admin{% endblock %}

{% block extrahead %}
    {{ block.super }}
    <link rel="icon" href="{% static 'img/favicon.png' %}" type="image/png">
{% endblock %}

{% block branding %}
<div id="branding">
    <h1 id="site-name">
        <a href="{% url 'admin:index' %}">Django Admin</a>
    </h1>
</div>
{% endblock %}

{% block usertools %}
    {{ block.super }}

    {% if request.user|in_group:"Users" %}
    <style>
        /* Hide only the Change Password link for Users group */
        #user-tools a[href$="password_change/"] {
            display: none !important;
        }
    </style>
    {% endif %}
{% endblock %}
```

**Key points:**

* Branding and logo are restored at the top left.
* Admin group sees everything, including “Change password.”
* Users group sees Logout but **cannot see Change password**.
* Favicon appears in browser tab.

---

## **3️⃣ apps/users/templatetags/group_filters.py**

**Purpose:** Provide a small helper filter for templates to check user group membership.

```python
from django import template

register = template.Library()

@register.filter
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
```

**Key points:**

* Used in templates with: `{% if request.user|in_group:"Users" %}`
* Makes role checks in templates clean and simple.
* Enables the `base_site.html` logic to hide Change password **only for Users group**.

---

## ✅ Summary of behavior

| User Type | Can View Users Table | Can Change Password | Branding/Logo | Logout |
| --------- | -------------------- | ------------------- | ------------- | ------ |
| Admin     | Yes                  | Yes                 | Yes           | Yes    |
| Users     | No                   | No                  | Yes           | Yes    |

**Benefits:**

* Clean role-based restrictions in Django Admin
* Branding and favicon intact
* Users cannot accidentally modify other users or change passwords
* Admin experience is unchanged

