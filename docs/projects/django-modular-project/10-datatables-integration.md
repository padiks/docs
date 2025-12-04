# **Guide 10 — DataTables Integration for UOM Module**

This guide explains how the **UOM module** has been enhanced to:

* Display **all records in a searchable, sortable, and paginated table** using **DataTables**.
* Allow users to **quickly navigate, filter, and manage records** without changing the base template layout.
* Integrate **DataTables JS and CSS** via CDN for simplicity and minimal setup.

We only have **two files** that need modifications to complete the integration.

> 💡 **Note:** Once this setup is applied for the UOM module, the same approach can be applied to other modules such as **Categories, Document Type, and Items** by updating their respective `base.html` and `index.html` files in the same way. This ensures consistent DataTables functionality across your entire app.

The repository includes a **sample SQLite database (`db.sqlite3`)** with preloaded tables and test data.

Available login credentials:

* **User account:** `user` / `demo`
* **Admin account:** `admin` / `root`

---

### **Affected Files**

Only **two files** need to be modified:

1. `base.html`
2. `apps/uom/templates/uom/index.html`

Below are the exact implementations:

---

### **1️⃣ base.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>{% load static %}
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Django Modular Project{% endblock %}</title>
    <link href="{% static 'img/favicon.png' %}" rel="icon" type="image/x-icon">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- DataTables CSS -->
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">		
    <link href="{% static 'css/style.css' %}?v=1.0.2" rel="stylesheet">
</head>
<body class="bg-light d-flex flex-column align-items-center">
<main class="container my-4">
    {% block content %}{% endblock %}
</main>
{% block footer %}
    {% include 'includes/footer.html' %}
{% endblock %}
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
{% block extra_js %}
    {% if user.is_authenticated %}
        <script src="{% static 'js/tableselect.js' %}"></script>
    {% endif %}
{% endblock %}
<!-- jQuery (required by DataTables) -->
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<!-- DataTables JS -->
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
<!-- Initialize DataTable -->
<script>
$(document).ready(function () {
    $('#itemsTable').DataTable({
        "pageLength": 10,
        "lengthMenu": [5, 10, 20, 50],
    });
});
</script>
</body>
</html>
```

---

### **2️⃣ apps/uom/templates/uom/index.html**

```django
{% extends 'base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="card shadow-lg p-4 mb-3">
    <!-- apps/uom/templates/uom/index.html -->
    <h4 class="mb-4 text-center">{{ title }}</h4>

    <div class="mb-3 d-flex flex-wrap align-items-center gap-2">
        <label for="tableSelect" class="form-label mb-0">Table:</label>

        {% include 'includes/_table_select.html' %}

        {% if user_group == 'Admin' %}
            <a href="{% url 'uom:add' %}" class="btn btn-success btn-sm" style="position: absolute; right: 25px;">Add</a>
        {% else %}
            <a href="#" class="btn btn-success btn-sm disabled" style="position: absolute; right: 25px;" title="View Only">Add</a>
        {% endif %}
    </div>

    <!-- DataTables id="itemsTable" for UOM records -->
    <div class="table-responsive">
        <table id="itemsTable" class="table table-sm table-striped table-bordered">
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

---

💡 **Summary:**

* `base.html` now includes **DataTables CSS & JS** and an initialization script.
* `index.html` table uses `id="itemsTable"` for DataTables to target.
* Pagination, sorting, and search are enabled automatically.
* Role-based access (`Admin` vs `User`) still applies for Add/Update/Delete buttons.

> ✅ This pattern can be repeated for **Categories, Document Type, Items**, or any module in your project. Just update the `table id` and corresponding `index.html` file.

---

### **Optional Tweak — Separate Footer for Clean `base.html`**

For a cleaner and more modular `base.html`, the footer has been moved to a separate file:

**In `base.html`:**

```django
{% block footer %}
    {% include 'includes/footer.html' %}
{% endblock %}
```

**In `templates/includes/footer.html`:**

```html
<footer class="attribution mt-auto py-3 bg-light text-center">
<p style="font-size: 1rem !important; margin: 0;">
    Credits: 
    <a href="https://getbootstrap.com/" target="_blank">Bootstrap</a>, 
    <a href="https://www.freepik.com/" target="_blank">Freepik</a>, 
    <a href="https://datatables.net/" target="_blank">DataTables</a>, 
    <a href="https://padiks.pythonanywhere.com" target="_blank">PythonAnywhere</a>, 
    <a href="https://www.djangoproject.com/" target="_blank">Django Project</a>.
    &mdash; 
    <a class="ln" href="{% url 'uom:index' %}">じゃんご</a>
    <a class="ln" href="{% url 'compute:index' %}">もでゅら</a>
    —
    {% if user.is_authenticated %}
        <a class="ln" href="{% url 'logout' %}">「ろぐあうと」</a>
    {% else %}
        <a class="ln" href="{% url 'login' %}">「ろぐいん」</a>
    {% endif %}
</p>
</footer>
```

**Benefits:**

* Keeps `base.html` cleaner and easier to maintain.
* Footer content is now reusable and easily editable across all pages.
* Dynamically shows login/logout links based on authentication status.

---

### **Optional Tweak — Global `tableSelect` JS for Logged-In Users**

The `tableSelect` functionality, previously inline in templates, has been **minified and moved to a separate JS file** (`static/js/tableselect.js`) to be reused globally in `base.html`.

**In `base.html`:**

```django
{% block extra_js %}
    {% if user.is_authenticated %}
        <script src="{% static 'js/tableselect.js' %}"></script>
    {% endif %}
{% endblock %}
```

**Key Points:**

* The script only loads for **authenticated users**.
* Users can select different tables from the dropdown (`_table_select.html`) and navigate automatically.
* Keeps the template cleaner and allows global reuse of the table selection logic.

**Example `_table_select.html`:**

```django
<select class="form-select form-select-sm" id="tableSelect" style="width: auto; min-width: 150px;">
    {% for table in tables %}
        <option value="{{ table }}" {% if table == current_table %}selected{% endif %}>
            {{ table }}
        </option>
    {% endfor %}
</select>

{% if user_group == 'Admin' %}
    <a href="{% url 'admin:index' %}" class="btn btn-white btn-sm custom-outline">Admin Group</a>
{% else %}
    <a href="{% url 'admin:index' %}" class="btn btn-white btn-sm custom-outline">User Group</a>
{% endif %}
```

**Benefits:**

* Centralizes table navigation logic in one JS file.
* Prevents unnecessary scripts from loading for non-logged-in users.
* Keeps templates modular and maintainable.
