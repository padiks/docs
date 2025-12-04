**📘 Django App Guide 4: Add 2nd Table (Categories) & Include Partial Template Globally**

This guide shows how to **add a second table to your Django project** by copying the structure of an existing table (in this case, `UOM`) and modifying it to create a new, independent app (`Categories`). The process can be repeated as many times as needed to add more tables without affecting existing apps.

It also demonstrates how to **include a partial template globally** using Django's `{% include %}` tag, allowing you to reuse common interface elements like table selectors, buttons, or headers across multiple apps, ensuring a consistent look and reducing duplication in your templates.

By the end of this guide, you will be able to:

* ✅ Duplicate and adapt an existing CRUD app for a new table.
* ✅ Maintain independent routes, forms, and views for each table.
* ✅ Include reusable template parts for shared UI components.
* ✅ Handle automatic timestamps (`created_at` and `updated_at`) for new records.
* ✅ Keep full control over your database without creating new tables manually.

### *(Using `models.py`, `forms.py`, existing SQLite table `stock_items_categories`, and reusable partial templates)*

This guide shows how to build a Django app that:

* ✅ Displays all `stock*` tables for reference (read-only)
* ✅ CRUD for `stock_items_categories`
* ✅ Uses separate routes for Add / Update
* ✅ Auto-saves `created_at` and `updated_at`
* ✅ Uses a `select` for Status
* ✅ Includes a reusable partial template (`_table_select.html`) globally
* ❌ Does NOT create or modify existing tables
* ❌ Does NOT create a new database — SQLite database is provided

This guide continues from **Guide 3** and focuses on **adding the Categories app** and using **partial templates** for code reuse.

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
│   ├── uom/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   └── templates/uom/
│   │       ├── index.html
│   │       └── form.html
│   │
│   └── categories/
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── forms.py
│       └── templates/categories/
│           ├── index.html
│           └── form.html
│
├── templates/
│   ├── base.html
│   └── includes/
│       └── _table_select.html      # Partial template for table selection
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

# 🧩 **2. Model for `stock_items_categories`**

### **`apps/categories/models.py`**

```python
from django.db import models

class StockItemCategories(models.Model):
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
        db_table = 'stock_items_categories'
        managed = False  # Do NOT let Django alter the table

    def __str__(self):
        return self.name
```

---

# 📝 **3. Form for Add/Update**

### **`apps/categories/forms.py`**

```python
from django import forms
from .models import StockItemCategories

class StockItemCategoriesForm(forms.ModelForm):
    STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive'),
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = StockItemCategories
        fields = ['name', 'description', 'status']  # created_at / updated_at excluded

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
```

---

# 🖥️ **4. Views**

### **`apps/categories/views.py`**

```python
import sqlite3
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import StockItemCategories
from .forms import StockItemCategoriesForm

DB_PATH = settings.BASE_DIR / 'db.sqlite3'

def index(request):
    # List all stock* tables for display only
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock%'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    records = StockItemCategories.objects.all().order_by('id')

    return render(request, 'categories/index.html', {
        'title': 'Categories List - Database db.sqlite3 / SQLite Tables',
        'records': records,
        'tables': tables,
        'current_table': 'stock_items_categories',
    })

def add_record(request):
    if request.method == 'POST':
        form = StockItemCategoriesForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            now = timezone.now()
            record.created_at = now
            record.updated_at = now
            record.save()
            return redirect('categories:index')
    else:
        form = StockItemCategoriesForm()

    return render(request, 'categories/form.html', {
        'title': 'Add Category',
        'form': form,
    })


def update_record(request, pk):
    record = get_object_or_404(StockItemCategories, pk=pk)

    if request.method == 'POST':
        form = StockItemCategoriesForm(request.POST, instance=record)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.updated_at = timezone.now()
            updated.save()
            return redirect('categories:index')
    else:
        form = StockItemCategoriesForm(instance=record)

    return render(request, 'categories/form.html', {
        'title': f'Update Category ID {record.id}',
        'form': form,
    })


def delete_record(request, pk):
    record = get_object_or_404(StockItemCategories, pk=pk)
    record.delete()
    return redirect('categories:index')
```

---

# 🌐 **5. URLs**

### **`apps/categories/urls.py`**

```python
from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_record, name='add'),
    path('update/<int:pk>/', views.update_record, name='update'),
    path('delete/<int:pk>/', views.delete_record, name='delete'),
]
```

Root `core/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.uom.urls')),            # Home app
    path('categories/', include('apps.categories.urls')),  # Categories app
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
```

---

# 🖌️ **6. Templates**

### **Partial Template — `_table_select.html`**

```html
<select class="form-select form-select-sm" id="tableSelect" style="width:auto; min-width:150px;">
    {% for table in tables %}
        <option value="{{ table }}" {% if table == current_table %}selected{% endif %}>{{ table }}</option>
    {% endfor %}
</select>
```

### **Index — `apps/categories/templates/categories/index.html`**

```html
{% extends 'base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="card shadow-lg p-4 mb-3">

    <h4 class="mb-4 text-center">{{ title }}</h4>

    <!-- Table selection + Add button -->
    <div class="mb-3 d-flex flex-wrap align-items-center gap-2">
        <label for="tableSelect" class="form-label mb-0">Table:</label>

        {% include 'includes/_table_select.html' %}

        <a href="{% url 'categories:add' %}" class="btn btn-success btn-sm" style="position: absolute; right: 25px;">Add</a>
    </div>

    <!-- Table with Categories records -->
    <div class="table-responsive">
        <table class="table table-sm table-striped table-bordered">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Description</th>
                    <th>Status</th>
                    <th>Created At</th>
                    <th>Updated At</th>
                    <th width="120">Actions</th>
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
                        <a href="{% url 'categories:update' row.id %}" class="btn btn-light btn-sm">Update</a>
                        <a href="{% url 'categories:delete' row.id %}"
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

### **Form — `apps/categories/templates/categories/form.html`**

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
        <a href="{% url 'categories:index' %}" class="btn btn-secondary btn-sm">Cancel</a>
    </form>
</div>
{% endblock %}
```

---

# 🎉 **Done!**

* Full CRUD for `stock_items_categories`
* Timestamps `created_at` and `updated_at` displayed, automatically added on creation
* Status dropdown selection
* Global partial template `_table_select.html` reused for table selector
* Add / Update forms exclude timestamps
* Delete inline with confirmation
* Existing SQLite DB only — no migrations needed
