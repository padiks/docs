# 📘 **Django App Guide 3: Full CRUD with dbpilot & UOM**

### *(Using `models.py`, `forms.py`, and existing SQLite tables — with add/update/delete and automatic timestamps)*

This guide shows how to build a Django app that:

* ✅ Displays all `stock*` tables for reference (read-only)
* ✅ CRUD for `stock_items_uom`
* ✅ Uses separate routes for Add / Update
* ✅ Auto-saves `created_at` and `updated_at`
* ✅ Uses a `select` for Status
* ❌ Does NOT create or modify existing tables
* ❌ Does NOT create a new database — SQLite database is provided

In this guide, we use **Django's ORM** (Object-Relational Mapping) to interact with the database without writing raw SQL. It allows us to manage database records easily through Python code, making it safer and faster to work with data like adding, updating, and deleting records.

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
│       ├── forms.py
│       ├── admin.py   # Optional
│       ├── tests.py   # Optional
│       └── templates/
│           └── uom/
│               ├── index.html
│               └── form.html
├── templates/
│   └── base.html
└── static/
│   ├── css/
│   └── img/
└── db.sqlite3                  
```

---

# ⚙️ **1. Configure SQLite in `settings.py`**

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

# 🧩 **2. Model for `stock_items_uom`**

### **`apps/uom/models.py`**

```python
from django.db import models

class StockItemUOM(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'stock_items_uom'
        managed = False  # Django will NOT create or alter this table

    def __str__(self):
        return self.name
```

---

# 📝 **3. Form for Add/Update**

### **`apps/uom/forms.py`**

```python
from django import forms
from .models import StockItemUOM

class StockItemUOMForm(forms.ModelForm):
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive'),
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = StockItemUOM
        fields = ['name', 'description', 'status']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
```

---

# 🖥️ **4. Views**

### **`apps/uom/views.py`**

```python
import sqlite3
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import StockItemUOM
from .forms import StockItemUOMForm

DB_PATH = settings.BASE_DIR / 'db.sqlite3'

def index(request):
    # List all stock* tables (read-only)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock%'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Active table: stock_items_uom
    records = StockItemUOM.objects.all().order_by('id')

    return render(request, 'uom/index.html', {
        'title': 'UOM List',
        'records': records,
        'tables': tables,
    })

def add_record(request):
    if request.method == 'POST':
        form = StockItemUOMForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.created_at = timezone.now()
            record.updated_at = timezone.now()
            record.save()
            return redirect('uom:index')
    else:
        form = StockItemUOMForm()
    return render(request, 'uom/form.html', {'title': 'Add UOM', 'form': form})

def update_record(request, pk):
    record = get_object_or_404(StockItemUOM, pk=pk)
    if request.method == 'POST':
        form = StockItemUOMForm(request.POST, instance=record)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.updated_at = timezone.now()
            updated.save()
            return redirect('uom:index')
    else:
        form = StockItemUOMForm(instance=record)
    return render(request, 'uom/form.html', {'title': f'Update UOM ID {record.id}', 'form': form})

def delete_record(request, pk):
    record = get_object_or_404(StockItemUOM, pk=pk)
    record.delete()
    return redirect('uom:index')
```

---

# 🌐 **5. URLs**

### **`apps/uom/urls.py`**

```python
from django.urls import path
from . import views

app_name = 'uom'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_record, name='add'),
    path('update/<int:pk>/', views.update_record, name='update'),
    path('delete/<int:pk>/', views.delete_record, name='delete'),
]
```

Root `core/urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    path('', include('apps.uom.urls')),
]
```

---

# 🖌️ **6. Templates**

### **Index — `apps/uom/templates/uom/index.html`**

```html
{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="card shadow-lg p-4 mb-3">
    <h4 class="mb-4 text-center">Database db.sqlite3 / SQLite Tables & UOM Records</h4>

    <!-- Table selector + Add button -->
    <div class="mb-3 d-flex flex-wrap align-items-center gap-2">
        <label for="tableSelect" class="form-label mb-0">Table:</label>
        <select class="form-select form-select-sm" id="tableSelect" style="width:auto; min-width:150px;">
            {% for table in tables %}
                <option value="{{ table }}" {% if table == 'stock_items_uom' %}selected{% endif %}>{{ table }}</option>
            {% endfor %}
        </select>
        <a href="{% url 'uom:add' %}" class="btn btn-success btn-sm">Add</a>
    </div>

    <!-- Records table -->
    <div class="table-responsive">
        <table class="table table-sm table-striped table-bordered">
            <thead>
                <tr>
                    <th>ID</th><th>Name</th><th>Description</th><th>Status</th>
                    <th>Created At</th><th>Updated At</th><th width="120">Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for row in records %}
                <tr>
                    <td>{{ row.id }}</td>
                    <td>{{ row.name }}</td>
                    <td>{{ row.description }}</td>
                    <td>{{ row.get_status_display }}</td>
                    <td>{{ row.created_at }}</td>
                    <td>{{ row.updated_at }}</td>
                    <td class="text-nowrap d-flex gap-1">
                        <a href="{% url 'uom:update' row.id %}" class="btn btn-light btn-sm">Update</a>
                        <a href="{% url 'uom:delete' row.id %}"
                           onclick="return confirm('Delete this record?')"
                           class="btn btn-light btn-sm">Delete</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
```

---

### **Form — `apps/uom/templates/uom/form.html`**

```html
{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="card shadow-lg p-4 mb-3">
    <h3 class="mb-4">{{ title }}</h3>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary btn-sm">Save</button>
        <a href="{% url 'uom:index' %}" class="btn btn-secondary btn-sm">Cancel</a>
    </form>
</div>
{% endblock %}
```

Got it! Here's how we can integrate that into the guide:

---

# 🎉 **Done!**

* Display all `stock*` tables
* Full CRUD for `stock_items_uom`
* Add / Update with separate forms
* Delete inline
* Automatic timestamps
* Status as a dropdown
* ORM-only — no raw SQL for CRUD
* Existing SQLite DB only — no migrations needed

### Optional: Using **Django Admin Integration** to Manage `StockItemUOM`

Once you add the following code to your `admin.py`, you can log into the Django admin interface at `http://localhost:8000/admin` and easily manage your `StockItemUOM` records. The project already includes a sample SQLite database with tables and data, so you don’t need to worry about setting up the database.

To access the Django admin interface, use one of the following accounts:

* **User account:**

  * **Username:** `user`
  * **Password:** `demo`

* **Admin account:**

  * **Username:** `admin`
  * **Password:** `root`

### `apps/uom/admin.py`

```python
from django.contrib import admin
from .models import StockItemUOM

class StockItemUOMAdmin(admin.ModelAdmin):
    # Make all fields read-only
    readonly_fields = ('id', 'name', 'description', 'status', 'created_at', 'updated_at')
    
    # Optionally, you can exclude certain fields from the admin form
    # exclude = ('field_to_exclude',)

    # If you want to make the model non-editable, you can define:
    # fields = ('name', 'description', 'status')  # and exclude other fields from admin
    
    # You can add more filters, ordering, or search fields here if needed
    search_fields = ['name']
    list_filter = ['status']
    list_display = ['name', 'status', 'created_at', 'updated_at']

admin.site.register(StockItemUOM, StockItemUOMAdmin)
```

Once you've added this to your `admin.py`, head over to `http://localhost:8000/admin` in your browser, log in with the provided credentials, and start managing your `StockItemUOM` records right from the admin panel.

This is entirely optional, but it can save time when working with large datasets!


