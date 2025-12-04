# 📘 **Django – Guide 15: Display Excel Data**

This guide walks you through setting up a **Django** application to **read and display Excel data** in a table format. You will learn how to use **`openpyxl`** to read Excel files, limit the displayed rows, and render the data in a Django template.

---

## 🎯 **Objectives**

By the end of this guide, you will:

* ✅ Set up a Django app to read Excel files
* ✅ Use **`openpyxl`** to open and extract data from `.xlsx` files
* ✅ Display the first 10 rows of data in a **table** on a Django page
* ✅ Handle errors if the Excel file is missing or unreadable
* ✅ Integrate the page with your existing navigation

---

## 📁 **Project Structure**

```
project_folder/
├── manage.py
├── core/
│   ├── settings.py              ← Project configuration
│   └── urls.py                  ← Core URL routing
│
├── apps/
│   ├── excel/                   ← App for Excel data
│   │   ├── apps.py
│   │   ├── views.py             ← Logic to read Excel
│   │   └── urls.py              ← App URLs
│
├── data/
│   └── excel.xlsx               ← Excel file to read
```

---

## 1️⃣ **Create the Excel App**

If you haven’t already created the app:

```bash
# Create the app
python manage.py startapp excel

# Move it to the apps folder
mv excel apps/
```

---

## 2️⃣ **Install Required Packages**

You need `openpyxl` to read `.xlsx` files:

```bash
pip install openpyxl
```

---

## 3️⃣ **Configure Settings**

In `core/settings.py`, add the app to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # Other apps
    'apps.compute',
    'apps.excel',        # Add this line
    'apps.api',
    'rest_framework',
    'apps.consumer',
]
```

Must match with `core/settings.py`

```python
# apps/excel/apps.py
from django.apps import AppConfig

class ExcelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.excel'
```

---

## 4️⃣ **Set Up App URLs**

Create `apps/excel/urls.py`:

```python
from django.urls import path
from . import views

app_name = 'excel'

urlpatterns = [
    path('', views.index, name='index'),
]
```

Then include it in `core/urls.py`:

```python
urlpatterns = [
    # Other paths...
    path('excel/', include('apps.excel.urls')),
]
```

---

## 5️⃣ **Create the View**

`apps/excel/views.py` reads the Excel file and passes data to the template:

```python
from django.shortcuts import render
import os
from django.conf import settings
from openpyxl import load_workbook

def index(request):
    file_path = os.path.join(settings.BASE_DIR, 'data', 'excel.xlsx')
    xlsx_data = []

    try:
        wb = load_workbook(filename=file_path)
        ws = wb.active

        # Display first 10 rows
        for row in ws.iter_rows(min_row=1, max_row=10, values_only=True):
            xlsx_data.append({
                "id": row[0],
                "member": row[1],
                "targets": row[2],
                "versus": row[3],
                "total": row[4],
            })

        context = {"title": "Excel Data", "xlsx": xlsx_data}

    except Exception as e:
        context = {"title": "Excel Data", "xlsx": [], "error": f"Failed to read Excel file: {e}"}

    return render(request, 'excel/index.html', context)
```

---

## 6️⃣ **Create the Template**

`apps/excel/templates/excel/index.html`:

```django
{% extends 'base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="card shadow-lg p-4 mb-3">
    <h4 class="mb-4 text-center">{{ title }}</h4>

    {% if error %}
        <div class="alert alert-danger">{{ error }}</div>
    {% endif %}

    {% block nav %}
        {% include 'includes/_compute_nav.html' %}
    {% endblock %}

    <div class="table-responsive">
        <table class="table table-sm table-striped table-bordered">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Member</th>
                    <th>Targets</th>
                    <th>Versus</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
                {% if xlsx %}
                    {% for excel in xlsx %}
                    <tr>
                        <td>{{ excel.id }}</td>
                        <td>{{ excel.member }}</td>
                        <td>{{ excel.targets }}</td>
                        <td>{{ excel.versus }}</td>
                        <td>{{ excel.total }}</td>
                    </tr>
                    {% endfor %}
                {% else %}
                    <tr>
                        <td colspan="5">No xlsx file available.</td>
                    </tr>
                {% endif %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
```

---

## 7️⃣ **Navigation Integration**

Make sure `_compute_nav.html` includes a link to Excel data:

```django
<li class="nav-item">
    <a class="nav-link border" href="{% url 'excel:index' %}">Excel Data</a>
</li>
```

---

✅ **Congratulations!**

You can now visit **`/excel/`** in your browser to view the first 10 rows of your Excel file.
