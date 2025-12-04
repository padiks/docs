# 📘 **Django – Guide 14: Rest API Consumer**

This guide walks you through setting up a **Django** application to **consume data** from an external REST API. You will learn how to fetch data from an external API (in this case, a public API that provides a list of books) and display it in your Django application.

---

## 🎯 **Objectives**

By the end of this guide, you will:

* ✅ Set up a Django app to consume data from an external API
* ✅ Use the `requests` library to make API requests
* ✅ Display fetched data in a Django template
* ✅ Learn how to display the data in a table format using **DataTables**
* ✅ Optionally, handle errors when the API is unavailable

---

## 📁 **Project Structure**

```
project_folder/
├── manage.py
├── core/
│   ├── settings.py              ← Settings for the project configuration
│   └── urls.py                  ← Core URL routing
│
├── apps/
│   ├── api/
│   ├── consumer/                ← New app for consuming external API
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py            ← Optional if needed
│   │   ├── views.py             ← Logic for fetching API data and rendering it
│   │   └── urls.py              ← URLs for the consumer app
│
```

---

## 1️⃣ **Create the Consumer App**

If you haven’t already created the **consumer** app, use the following commands:

```bash
# Create the app
python manage.py startapp consumer

# Move it to the apps folder
mv consumer apps/
```

---

## 2️⃣ **Install Required Packages**

Make sure that you have the **requests** library installed, as it will be used to fetch data from the external API.

```bash
pip install requests
```

---

## 3️⃣ **Configure Settings**

In the `settings.py` file, add the new `consumer` app and `rest_framework` to the `INSTALLED_APPS` list:

```python
INSTALLED_APPS = [
    # Other apps
    'apps.api',
    'rest_framework',
    'apps.consumer',  # Add this line
]
```

---

## 4️⃣ **Update URLs**

In the `urls.py` file of the core folder (`core/urls.py`), add a new path for the consumer app:

```python
urlpatterns = [
    # Other paths
    path('consumer/', include('apps.consumer.urls')),  # Consumer path for Rest API Framework
]
```

---

## 5️⃣ **Create Views to Consume the API**

In the `apps/consumer/views.py` file, use the `requests` library to fetch data from the external API:

```python
import requests
from django.shortcuts import render

def index(request):
    # Fetch data from the external API
    api_url = "https://padiks.pythonanywhere.com/api/books/"
    response = requests.get(api_url)

    if response.status_code == 200:
        # Since the API returns a list of books, we can directly assign the list to books_data
        books_data = response.json()  # No need to use .get() here, as the response is a list
        context = {
            'title': 'Books List',
            'books': books_data,  # Passing the list directly
        }
    else:
        context = {
            'title': 'Books List',
            'books': [],
            'error': 'Failed to fetch data from API'
        }

    return render(request, 'consumer/index.html', context)
```

---

## 6️⃣ **Create the Consumer URLs**

In the `apps/consumer/urls.py` file, map the `index` view to a URL:

```python
from django.urls import path
from . import views

app_name = 'consumer'

urlpatterns = [
    path('', views.index, name='index'),
]
```

---

## 7️⃣ **Create the Template for Displaying Data**

In the `apps/consumer/templates/consumer/index.html` file, display the fetched data in a table format:

```html
{% extends 'base.html' %}

{% block title %}{{ title }} - Rest API Consumer{% endblock %}

{% block content %}
<div class="card shadow-lg p-4 mb-3">
    <h4 class="mb-4 text-center">{{ title }} - Rest API Consumer</h4>

    {% if error %}
        <div class="alert alert-danger">{{ error }}</div>
    {% endif %}

    <div class="mb-3 d-flex flex-wrap align-items-center gap-2">
        <a href="https://padiks.pythonanywhere.com/api/books/" 
           class="btn btn-success btn-sm" 
           style="position: absolute; right: 25px; margin-bottom:10px;" 
           title="Books List - Fetched from External API">
           Rest API Framework
        </a>
    </div>

    <div class="table-responsive">
        <table id="itemsTable" class="table table-sm table-striped table-bordered">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Author</th>
                    <th>Published Date</th>
                </tr>
            </thead>
            <tbody>
                {% if books %}
                    {% for book in books %}
                    <tr>
                        <td>{{ book.id }}</td>
                        <td>{{ book.title }}</td>
                        <td>{{ book.author }}</td>
                        <td>{{ book.published_date }}</td>
                    </tr>
                    {% endfor %}
                {% else %}
                    <tr>
                        <td colspan="4">No books available.</td>
                    </tr>
                {% endif %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
```

---

## 8️⃣ **Testing the Consumer**

Once everything is set up, you can visit the URL for the **consumer** app, typically `http://localhost:8000/consumer/`, and you should see the list of books fetched from the external API displayed in a table.

---

## Summary

In **Guide 14**, we covered how to set up a Django app to **consume data from an external API** using the **requests** library. By following the steps above, we were able to display the books fetched from the external API (`https://padiks.pythonanywhere.com/api/books/`) in a table on our site.

You can easily extend this guide to consume other APIs, display more complex data, or implement error handling for various response scenarios.

