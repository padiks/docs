# 📘 **Django – Guide 13: REST API Framework**

This guide walks you through setting up a **Django Rest Framework (DRF)**-based API to manage data such as books. By following the steps in this guide, you'll learn how to create the API views, serializers, and set up the required routing.

---

## 🎯 **Objectives**

By the end of this guide, you will:

* ✅ Set up a RESTful API using Django Rest Framework (DRF)
* ✅ Implement basic CRUD functionality (Create, Read, Update, Delete) for the `Book` model
* ✅ Set up routing and views for handling API requests
* ✅ Learn how to serialize model data and respond with JSON
* ✅ Test the API using browser, Postman, or curl
* ✅ Optionally add authentication using Token-based or JWT Authentication

---

## 📁 **Project Structure**

```
project_folder/
├── manage.py
├── core/
│   ├── settings.py              ← Settings for DRF and project configuration
│   └── urls.py                  ← Core URL routing
│
├── apps/                                  
│   ├── api/                             
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py                ← Define the Book model here
│   │   ├── serializers.py           ← Define serializers for the model
│   │   ├── views.py                 ← Views to handle API logic
│   │   └── urls.py                  ← Define the API routes
│
└── db.sqlite3                       ← SQLite database (optional for testing)
```

---

## 1️⃣ **Install Django Rest Framework (DRF)**

If you haven't already installed DRF, you can do so using the following:

```bash
# Change to the project folder, regardless of where it resides
cd /home/user/Public/web/project_folder
python3 -m venv venv
source venv/bin/activate

pip install djangorestframework
```

Then, add `'rest_framework'` to the `INSTALLED_APPS` in your `settings.py` file:

```python
# core/settings.py
INSTALLED_APPS = [
    # Other apps
    'rest_framework',    # Add Django Rest Framework
    'apps.api',           # Include the API app
]
```

---

## 2️⃣ **Create the API App**

Run the following commands to create a new API app and add it to the `apps` directory:

```bash
python manage.py startapp api
mv api apps/
```

Define the app configuration in `apps.py`:

```python
# apps/api/apps.py
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.api'
```

---

## 3️⃣ **Define the `Book` Model**

Create the `Book` model inside `models.py`. This model will represent a book in the database.

```python
# apps/api/models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    def __str__(self):
        return self.title
```

After creating the model, run migrations to apply the changes:

```bash
python manage.py makemigrations api
python manage.py migrate
```

---

## 4️⃣ **Create the Serializer**

Next, create a **serializer** to convert the `Book` model into JSON format. This will allow the model data to be passed between Django and the API.

Create the `serializers.py` file in the `api` app:

```python
# apps/api/serializers.py
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Serialize all fields from the Book model
```

---

## 5️⃣ **Create the API Views**

Use Django REST Framework's `ModelViewSet` to automatically provide CRUD operations for the `Book` model. Create the views in `views.py`:

```python
# apps/api/views.py
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()  # All books
    serializer_class = BookSerializer  # Link to the serializer
```

---

## 6️⃣ **Define URLs for the API**

In the `api/urls.py` file, define the URL routing for the API endpoints. We use Django REST Framework's `DefaultRouter` to handle routing automatically.

```python
# apps/api/urls.py
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

app_name = 'api'  # Set the app namespace

router = DefaultRouter()
router.register(r'books', BookViewSet)  # Register BookViewSet for CRUD

# Use the generated URL patterns
urlpatterns = router.urls
```

This will automatically generate the following routes:

* **GET** `/api/books/` - List all books
* **POST** `/api/books/` - Create a new book
* **GET** `/api/books/{id}/` - Retrieve a book by ID
* **PUT** `/api/books/{id}/` - Update a book by ID
* **DELETE** `/api/books/{id}/` - Delete a book by ID

---

## 7️⃣ **Include the API URLs in Core `urls.py`**

Now include the `api/urls.py` in your core project's `urls.py`:

```python
# core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Other URLs
    path('api/', include('apps.api.urls')),  # Include the API URLs
]
```

This makes sure that any requests starting with `/api/` will be routed to the API app.

---

## 8️⃣ **Update the Compute Template**

In your **Compute** module template, update the navigation to link to the API documentation or a relevant API page:

```html
<!-- templates/includes/_compute_nav.html -->
<div class="mb-3">
    <ul class="nav justify-content-center">
        <li class="nav-item">
            <a class="nav-link border" href="{% url 'compute:summation' %}">Summation</a>
        </li>
        <li class="nav-item">
            <a class="nav-link border" href="{% url 'compute:summary' %}">Alpine.js</a>
        </li>
        <li class="nav-item">
            <a class="nav-link border" href="{% url 'api:book-list' %}">Rest Framework</a>
        </li>		
    </ul>
</div>
```

---

## 9️⃣ **Test the API**

Now that the API is set up, you can run your server and test the API routes:

```bash
python manage.py runserver
```

**Test the API with**:

1. **GET** `/api/books/` - List all books

2. **POST** `/api/books/` - Create a new book by sending data as JSON:

   ```json
   {
       "title": "The Great Gatsby",
       "author": "F. Scott Fitzgerald",
       "published_date": "1925-04-10"
   }
   ```

3. **GET** `/api/books/1/` - Retrieve a book by ID.

4. **PUT** `/api/books/1/` - Update a book.

5. **DELETE** `/api/books/1/` - Delete a book.

---

## 🔒 **Authentication (Optional)**

If you want to add authentication to your API, you can use Token Authentication or JWT Authentication. Here's an optional setup for JWT:

1. **Install JWT Authentication**:

   ```bash
   pip install djangorestframework-simplejwt
   ```

2. **Update `settings.py`** for JWT Authentication:

   ```python
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework_simplejwt.authentication.JWTAuthentication',
       ],
   }
   ```

3. **Add Token Views to `urls.py`**:

   ```python
   # core/urls.py
   from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

   urlpatterns += [
       path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
       path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   ]
   ```

---

### 🔐 Testing JWT Authentication

You can use the following login credentials to test **Token Obtain Pair** (`/api/token/`) and **Token Refresh** (`/api/token/refresh/`):

#### **Available login credentials**

**Regular User**

* **Username:** `user`
* **Password:** `demo`

**Admin User**

* **Username:** `admin`
* **Password:** `root`

These accounts can be used with:

```
POST /api/token/
{
    "username": "<username>",
    "password": "<password>"
}
```

To get:

* **Access Token**: Short-lived token used for authentication (usually minutes to hours).
* **Refresh Token**: Long-lived token that lets you request a **new access token** after it expires.

You can then use:

```
POST /api/token/refresh/
{
    "refresh": "<refresh_token_here>"
}
```

To obtain a new **access token**.

---

## 🎯 **Conclusion**

In this guide, you've successfully set up a simple **Django Rest Framework (DRF)** API for managing books. You learned how to:

* Define the `Book` model
* Serialize the model with a `BookSerializer`
* Create views for CRUD operations using a `BookViewSet`
* Define the URL routes for the API
* Test the API and optionally add authentication

This sets the foundation for adding more complex APIs to your project, whether for other models or advanced features like pagination, filtering, and authentication.
