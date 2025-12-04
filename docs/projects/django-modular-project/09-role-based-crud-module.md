# **Guide 9 — Role-Based CRUD for UOM Module (Users vs Admin Group)**

This guide explains how the **UOM module** has been customized to:

* Allow **Admins** full CRUD access (Add, Update, Delete).
* Restrict **Users group** to **view-only**, preventing any changes in the database.
* Disable buttons in the UI for Users group for a visual cue.
* Keep the standard template layout intact.

We only have **two working files** for this customization.

> 💡 **Note:** Once this logic is implemented for the UOM module, the same approach can be applied to other modules such as **Categories, Document Type, and Items** by updating their respective `views.py` and `index.html` files in the same way. This ensures consistent role-based access across your entire app.

The repository includes a **sample SQLite database (`db.sqlite3`)** with preloaded tables and test data.

Available login credentials:

* **User account:** `user` / `demo`
* **Admin account:** `admin` / `root`

---

## **1️⃣ apps/uom/views.py**

**Purpose:** Handle all CRUD operations for `StockItemUOM` with role-based restrictions.

```python
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import sqlite3
from .models import StockItemUOM
from .forms import StockItemUOMForm

DB_PATH = settings.BASE_DIR / 'db.sqlite3'


@login_required
def index(request):
    # Get logged-in user's primary group
    user_groups = request.user.groups.values_list('name', flat=True)
    user_group = user_groups[0] if user_groups else None

    # List all stock* tables for display only
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock%'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Only records for stock_items_uom
    records = StockItemUOM.objects.all().order_by('id')

    return render(request, 'uom/index.html', {
        'title': 'Stock Items UOM List',
        'records': records,
        'tables': tables,
        'current_table': 'stock_items_uom',
        'user_group': user_group,
    })


@login_required
def add_record(request):
    # Users group cannot add
    if not (request.user.is_superuser or request.user.groups.filter(name='Admin').exists()):
        messages.warning(request, "You do not have permission to add UOM records.")
        return redirect('uom:index')

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

    return render(request, 'uom/form.html', {
        'title': 'Add UOM',
        'form': form,
    })


@login_required
def update_record(request, pk):
    record = get_object_or_404(StockItemUOM, pk=pk)

    # Users group cannot edit
    if not (request.user.is_superuser or request.user.groups.filter(name='Admin').exists()):
        messages.warning(request, "You do not have permission to edit UOM records.")
        return redirect('uom:index')

    if request.method == 'POST':
        form = StockItemUOMForm(request.POST, instance=record)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.updated_at = timezone.now()
            updated.save()
            return redirect('uom:index')
    else:
        form = StockItemUOMForm(instance=record)

    return render(request, 'uom/form.html', {
        'title': f'Update UOM ID {record.id}',
        'form': form,
    })


@login_required
def delete_record(request, pk):
    record = get_object_or_404(StockItemUOM, pk=pk)

    # Users group cannot delete
    if not (request.user.is_superuser or request.user.groups.filter(name='Admin').exists()):
        messages.warning(request, "You do not have permission to delete UOM records.")
        return redirect('uom:index')

    record.delete()
    return redirect('uom:index')
```

**Key points:**

* Admin group → full CRUD access.
* Users group → **cannot add, edit, or delete**.
* Backend ensures Users group cannot bypass the view and save data.
* Messages inform Users group that they lack permission.

---

## **2️⃣ apps/uom/templates/uom/index.html**

**Purpose:** Display the UOM list table with buttons disabled for Users group.

```django
{% extends 'base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="card shadow-lg p-4 mb-3">
<!-- apps/uom/templates/uom/index.html -->
    <h4 class="mb-4 text-center">{{ title }}</h4>

    <!-- Table selection + Add button -->
    <div class="mb-3 d-flex flex-wrap align-items-center gap-2">
        <label for="tableSelect" class="form-label mb-0">Table:</label>

        {% include 'includes/_table_select.html' %}

        {% if user_group == 'Admin' %}
            <a href="{% url 'uom:add' %}" class="btn btn-success btn-sm" style="position: absolute; right: 25px;">Add</a>
        {% else %}
            <a href="#" class="btn btn-success btn-sm disabled" style="position: absolute; right: 25px;" title="View Only">Add</a>
        {% endif %}
    </div>

    <!-- Table with UOM records -->
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
                        {% if user_group == 'Admin' %}
                            <a href="{% url 'uom:update' row.id %}" class="btn btn-light btn-sm">Update</a>
                            <a href="{% url 'uom:delete' row.id %}" onclick="return confirm('Delete this record?')" class="btn btn-light btn-sm">Delete</a>
                        {% else %}
                            <a href="#" class="btn btn-light btn-sm disabled" title="View Only">Update</a>
                            <a href="#" class="btn btn-light btn-sm disabled" title="View Only">Delete</a>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

</div>
{% endblock %}
```

**Key points:**

* Buttons **Add, Update, Delete** are disabled for Users group.
* Table is **read-only** for Users group.
* Admin group sees all buttons and can perform CRUD operations.
* Works together with `views.py` role checks for backend enforcement.

---

## ✅ Summary of behavior

| User Type | Can View Table | Can Add | Can Edit | Can Delete | Buttons Disabled |
| --------- | -------------- | ------- | -------- | ---------- | ---------------- |
| Admin     | Yes            | Yes     | Yes      | Yes        | No               |
| Users     | Yes            | No      | No       | No         | Yes              |

**Benefits:**

* Clean, modular, role-based CRUD in Django views.
* Users group is safely restricted while still able to view data.
* Admin group has full control.
* Minimal changes — only **views.py** and **index.html** are updated.
