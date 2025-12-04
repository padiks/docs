# 📘 **Django App Guide 2: dbpilot with uom, base.html, and SQLite3**

### *(Using `models.py` but WITHOUT creating tables — reading existing SQLite tables)*

This guide shows how to build a Django app that:

* ✅ Uses `base.html`
* ✅ Uses your existing SQLite database
* ✅ Connects to an existing table (`stock_items_uom`)
* ✅ Reads/dumps data using Django ORM
* ❌ Does NOT create or modify the table
* ❌ Does NOT run migrations for this table
* ❌ Does NOT create or modify the database. The SQLite database is already provided in the repository with sample data

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
│   └── uom/
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       └── templates/
│           └── uom/
│               └── index.html
├── templates/
│   └── base.html
└── static/
│   ├── css/
│   │   └── style.css       
│   └── img/
│       └── favicon.png 
└── db.sqlite3                  
```

---

# ⚙️ **1. Configure SQLite in `settings.py`**

Make sure your database is set like this:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

✔ No migrations needed for existing tables.

---

# 🧩 **2. Create a Model for the Existing Table**

Django must know the schema so it can read rows.
But we prevent Django from creating or modifying the table using:

```python
managed = False
```

---

### **`apps/uom/models.py`**

```python
from django.db import models

class StockItemUOM(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'stock_items_uom'  # Use your exact table name
        managed = False               # <-- Django will NOT create or alter this table

    def __str__(self):
        return self.name
```

### ✔ What this does:

* Maps Django ORM → to an **existing** SQLite table
* No migration needed
* You can run `StockItemUOM.objects.all()`
* Django reads data normally
* Zero risk of Django editing the schema

---

# 🖥️ **3. Dump Data Using Django ORM**

This view reads from the existing table and sends the data to the template.

### **`apps/uom/views.py`**

```python
from django.shortcuts import render
from .models import StockItemUOM

def index(request):
    records = StockItemUOM.objects.all()  # ORM reading real rows

    return render(request, 'uom/index.html', {
        'title': 'UOM Home',
        'welcome_message': 'Dumping Data via Django ORM',
        'records': records,
    })
```

✔ Super clean
✔ ORM-only
✔ No raw SQL

---

# 🌐 **4. Add URL Route**

### **`apps/uom/urls.py`**

```python
from django.urls import path
from . import views

app_name = 'uom'

urlpatterns = [
    path('', views.index, name='index'),
]
```

### Root router (`core/urls.py`):

```python
path('', include('apps.uom.urls')),
```

---

# 🎨 **5. Display the Data in the Template**

Inside **`apps/uom/templates/uom/index.html`:**

```html
{% extends 'base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<h4 class="mb-3">SQLite Data Dump (Using Model)</h4>

<table class="table table-bordered table-striped">
  <thead>
    <tr>
      <th>ID</th>
      <th>Name</th>
      <th>Description</th>
      <th>Status</th>
      <th>Created</th>
    </tr>
  </thead>
  <tbody>
    {% for row in records %}
    <tr>
      <td>{{ row.id }}</td>
      <td>{{ row.name }}</td>
      <td>{{ row.description }}</td>
      <td>{{ row.status }}</td>
      <td>{{ row.created_at }}</td>
    </tr>
    {% empty %}
    <tr>
      <td colspan="5" class="text-center text-muted">No data found</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
```

✔ Uses your current layout
✔ No design changes required
✔ Simple data dump

---

# 🎉 **Done!**

You now have:

* Django reading your existing SQLite DB
* Models that map to tables without migration
* Data dumping on a clean template
* Base template layout supported
* A minimal, professional, GitHub-ready project

### Only 2 core steps:

### ✔ `models.py` → add model with `managed=False`

### ✔ `views.py` → dump using ORM with `.objects.all()`
