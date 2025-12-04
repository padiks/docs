# 📘 Django – Guide 7: User Management, Admin Customization & Role-Based Groups

> **📌 Note:**
>This guide continues from **Guide 6: Authentication**. However, it is a complete, standalone collection of all files from the previous guides, so you can start here and everything will work correctly.

---

## 🎯 Objectives

By the end of this guide, you will:

* ✅ Create and manage superusers & normal users
* ✅ Use **Groups** to separate roles (Admin / Users)
* ✅ Customize Django Admin using groups
* ✅ Make **UOM** visible to normal users (read-only)
* ❌ Hide all other tables (Items, Categories, etc.) from normal users
* ✅ Give Admin full access to everything

---

## 📁 Project Structure (Relevant Files)

```
project_folder/
├── apps/
│   ├── users/
│   │   ├── admin.py       ← Customize User list
│   │   └── templates/users/login.html
│   ├── uom/
│   │   ├── admin.py       ← Admin full CRUD, Users read-only
│   │   ├── views.py       ← Role-based template logic
│   │   └── templates/uom/index.html
│   ├── items/
│   │   ├── admin.py       ← Hidden from normal users
│   │   └── views.py
│   ├── categories/
│   │   ├── admin.py       ← Hidden from normal users
│   │   └── views.py
├── core/
│   └── urls.py
└── db.sqlite3
```

---

## 1️⃣ Creating a Superuser

```bash
python manage.py createsuperuser
```

Sample database already includes:

| Account | Username | Password |
| ------- | -------- | -------- |
| Admin   | `admin`  | `root`   |
| User    | `user`   | `demo`   |

---

## 2️⃣ Changing User Passwords

### Using Admin Panel

1. Go to `/admin/`
2. Click **Users**
3. Select a user
4. Click **Change Password**

### Using Django Shell

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
u = User.objects.get(username='user')
u.set_password('newpass')
u.save()
```

---

## 3️⃣ Customizing User List Display

`apps/users/admin.py`

```python
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin   # <-- IMPORTANT

class CustomUserAdmin(UserAdmin):
    # Display key fields to distinguish admins vs users
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')


# Unregister default User admin
admin.site.unregister(User)

# Register custom admin that still includes password change + profile
admin.site.register(User, CustomUserAdmin)
```

> ✅ Shows admin/staff status, activity, and groups at a glance.

---

## 4️⃣ Role-Based Groups: Admin & Users

### Create Two Groups

1. Open `/admin/ → Groups`
2. Add **Admin**
3. Add **Users**
4. No permissions needed—simple setup for beginners

### Assign Users to Groups

| User                 | Group |
| -------------------- | ----- |
| admin                | Admin |
| user / user1 / user2 | Users |

### Simple Check in Code

```python
if request.user.groups.filter(name='Admin').exists():
    # Admin logic
else:
    # User logic
```

---

## 5️⃣ UOM Admin & Role-Based Template

### `apps/uom/admin.py`

```python
from django.contrib import admin
from .models import StockItemUOM

class StockItemUOMAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['status']

    readonly_fields = (
        'id', 'name', 'description', 'status',
        'created_at', 'updated_at'
    )

    # Users → read-only, Admin → full CRUD
    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Admin').exists():
            return ('id', 'created_at', 'updated_at')
        return self.readonly_fields

    def has_add_permission(self, request):
        return request.user.groups.filter(name='Admin').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='Admin').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='Admin').exists()

admin.site.register(StockItemUOM, StockItemUOMAdmin)
```

---

### `apps/uom/views.py`

```python
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import sqlite3
from .models import StockItemUOM
from .forms import StockItemUOMForm

DB_PATH = settings.BASE_DIR / 'db.sqlite3'

@login_required
def index(request):
    # Get the logged-in user's primary group
    user_groups = request.user.groups.values_list('name', flat=True)
    user_group = user_groups[0] if user_groups else None

    # List all stock* tables
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock%'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Only UOM records
    records = StockItemUOM.objects.all().order_by('id')

    return render(request, 'uom/index.html', {
        'title': 'Stock Items UOM List',
        'records': records,
        'tables': tables,
        'current_table': 'stock_items_uom',
        'user_group': user_group,   # Pass to template
    })

@login_required
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

@login_required
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

@login_required
def delete_record(request, pk):
    record = get_object_or_404(StockItemUOM, pk=pk)
    record.delete()
    return redirect('uom:index')
```

---

### `apps/uom/templates/uom/index.html`

```html
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

<script>
document.getElementById('tableSelect').addEventListener('change', function() {
    const selectedTable = this.value;
    if (selectedTable === 'stock_items_categories') window.location.href = '/categories/';
    else if (selectedTable === 'stock_document_type') window.location.href = '/doctype/';
    else if (selectedTable === 'stock_items') window.location.href = '/items/';
    else if (selectedTable === 'stock_items_uom') window.location.href = '/';
});
</script>
```

> ✅ Admin sees “Admin Group” button, Users see “User Group” button. Users can view UOM but cannot CRUD.

> This same pattern can be **applied to other templates/modules**.

---

## 6️⃣ Hide All Other Tables From Users

In `apps/items/admin.py`, `apps/categories/admin.py`, etc.:

```python
def has_module_permission(self, request):
    return request.user.groups.filter(name='Admin').exists()
```

* Only Admins see these apps in Django Admin
* Users have view-only access to the UOM table; all other tables are hidden.

---

## 7️⃣ Login Template Reference

`apps/users/templates/users/login.html`

```html
<ul class="small text-muted">
    <li>User account: <code>user</code> / <code>demo</code></li>
    <li>Admin account: <code>admin</code> / <code>root</code></li>
</ul>
```

---

## 🎉 Final Result

| Feature             | Admin  | User        |
| ------------------- | ------ | ----------- |
| View all tables     | ✅ Yes  | ❌ No        |
| Edit all tables     | ✅ Yes  | ❌ No        |
| View UOM            | ✅ Yes  | ✅ Yes       |
| Edit UOM            | ✅ Yes  | ❌ Read-only |
| Access Django Admin | ✅ Yes  | ✅ Yes       |
| Role handled by     | Groups | Groups      |

