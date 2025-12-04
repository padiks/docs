# 📘 **Django - Guide 5: Add `Items` Table with Foreign Keys**

This guide demonstrates how to **create a new `Items` table** in your Django project and establish foreign key relationships to the **`Categories`** and **`UOM` (Units of Measure)** tables created in previous guides. It will cover the **CRUD functionality** for the `Items` table, including how to handle these foreign key relationships in your forms and templates.

By the end of this guide, you will be able to:

* ✅ **Create a new `Items` table** with foreign keys to `Categories` and `UOM`.
* ✅ Handle **foreign key relationships** to display category and UOM names instead of IDs.
* ✅ Build **CRUD views** for the `Items` table.
* ✅ Use **ModelForms** for adding and updating `Items` records.
* ✅ Reuse the **partial template** for table selection globally.

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
│   ├── categories/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   └── templates/categories/
│   │       ├── index.html
│   │       └── form.html
│   │
│   └── items/
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── forms.py
│       └── templates/items/
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

✔ **No migrations needed** for existing tables. We're working with a pre-existing database.

---

# 🧩 **2. Model for `Items` Table**

### **`apps/items/models.py`**

```python
from django.db import models

class StockItems(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive'),
    ]

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey('categories.StockItemCategories', on_delete=models.SET_NULL, null=True, blank=True)
    uom = models.ForeignKey('uom.StockItemUOM', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stock_items'
        managed = False  # Do NOT let Django alter the table

    def __str__(self):
        return self.code
```

---

# 📝 **3. Form for Add/Update**

### **`apps/items/forms.py`**

```python
from django import forms
from .models import StockItems
from categories.models import StockItemCategories
from uom.models import StockItemUOM

class StockItemsForm(forms.ModelForm):
    STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive'),
    ]

    # ForeignKey to StockItemCategories (Categories)
    category = forms.ModelChoiceField(
        queryset=StockItemCategories.objects.filter(status=1),  # Only show active categories
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='Select a category'
    )

    # ForeignKey to StockItemUOM (Units of Measure)
    uom = forms.ModelChoiceField(
        queryset=StockItemUOM.objects.all(),  # All UOMs are available
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='Select a UOM'
    )

    # Status dropdown (active or inactive)
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = StockItems
        fields = ['code', 'description', 'category', 'uom', 'status']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
```

---

# 🖥️ **4. Views**

### **`apps/items/views.py`**

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import StockItems
from .forms import StockItemsForm

def index(request):
    records = StockItems.objects.all().order_by('id')
    return render(request, 'items/index.html', {
        'title': 'Items List',
        'records': records,
    })

def add_record(request):
    if request.method == 'POST':
        form = StockItemsForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.created_at = timezone.now()
            record.updated_at = timezone.now()
            record.save()
            return redirect('items:index')
    else:
        form = StockItemsForm()

    return render(request, 'items/form.html', {
        'title': 'Add Item',
        'form': form,
    })

def update_record(request, pk):
    record = get_object_or_404(StockItems, pk=pk)
    if request.method == 'POST':
        form = StockItemsForm(request.POST, instance=record)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.updated_at = timezone.now()
            updated.save()
            return redirect('items:index')
    else:
        form = StockItemsForm(instance=record)

    return render(request, 'items/form.html', {
        'title': f'Update Item ID {record.id}',
        'form': form,
    })

def delete_record(request, pk):
    record = get_object_or_404(StockItems, pk=pk)
    record.delete()
    return redirect('items:index')
```

---

# 🌐 **5. URLs**

### **`apps/items/urls.py`**

```python
from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_record, name='add'),
    path('update/<int:pk>/', views.update_record, name='update'),
    path('delete/<int:pk>/', views.delete_record, name='delete'),
]
```

---

# 🖌️ **6. Templates**

### **Index — `apps/items/templates/items/index.html`**

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

        <a href="{% url 'items:add' %}" class="btn btn-success btn-sm" style="position: absolute; right: 25px;">Add Item</a>
    </div>

    <!-- Table with Items records -->
    <div class="table-responsive">
        <table class="table table-sm table-striped table-bordered">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Code</th>
                    <th>Description</th>
                    <th>Category</th>
                    <th>UOM</th>
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
                    <td>{{ row.code }}</td>
                    <td>{{ row.description }}</td>
                    <td>{{ row.category.name }}</td> <!-- Display category name -->
                    <td>{{ row.uom.name }}</td> <!-- Display UOM name -->
                    <td>{{ row.get_status_display }}</td>
                    <td>{{ row.created_at }}</td>
                   
```


 <td>{{ row.updated_at }}</td>
                    <td class="text-nowrap d-flex gap-1">
                        <a href="{% url 'items:update' row.id %}" class="btn btn-light btn-sm">Update</a>
                        <a href="{% url 'items:delete' row.id %}" onclick="return confirm('Delete this record?')" class="btn btn-light btn-sm">Delete</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

</div>
{% endblock %}
```

### **Form — `apps/items/templates/items/form.html`**

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
        <a href="{% url 'items:index' %}" class="btn btn-secondary btn-sm">Cancel</a>
    </form>
</div>
{% endblock %}
```

---

# 🎉 **Done!**

* Full CRUD for `Items` table with **foreign keys** to `Categories` and `UOM`
* **Timestamps** `created_at` and `updated_at` automatically set
* **Category** and **UOM** names displayed in the table
* Reused the **partial template** `_table_select.html` for table selection
* **No migrations required**—working with an existing SQLite database

