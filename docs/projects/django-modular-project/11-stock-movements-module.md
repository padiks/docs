# 📘 Django – Guide 11: Stock Movements Module

> **📌 Note:**
> This guide is standalone and shows all modifications for the **Stock Movements module**, including date formatting, Admin-only actions, and table navigation.

The repository includes a **sample SQLite database (`db.sqlite3`)** with preloaded tables and test data.

Available login credentials:

* **User account:** `user` / `demo`
* **Admin account:** `admin` / `root`

---

## 🎯 Objectives

By the end of this guide, you will:

* ✅ Display **all stock movement records** in a sortable table
* ✅ Format **movement date** as `DD/MM/YYYY`
* ✅ Format **updated at** as `DD Mon. YYYY, g:i a`
* ✅ Restrict add/update/delete actions to **Admin users** only
* ✅ Integrate **central table navigation** with a dropdown selector
* ❌ Normal users cannot edit or delete records

---

## 📁 Project Structure (Relevant Files)

```
project_folder/
├── apps/
│   ├── movements/
│   │   ├── models.py       ← StockMovements model with timestamps
│   │   ├── forms.py        ← StockMovementsForm with datetime-local
│   │   ├── views.py        ← CRUD + Admin-only permissions
│   │   ├── urls.py         ← Module URLs
│   │   └── templates/movements/
│   │       ├── index.html  ← List view table
│   │       └── form.html   ← Add/Update form
├── core/
│   └── urls.py
└── db.sqlite3
```

---

## 1️⃣ `core/urls.py` — Routing

```python
urlpatterns = [
    path('uom/', include('apps.uom.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('categories/', include('apps.categories.urls')),
    path('doctype/', include('apps.doctype.urls')),
    path('items/', include('apps.items.urls')),
    path('compute/', include('apps.compute.urls')),
    path('movements/', include('apps.movements.urls')),        
    path('', include('apps.movements.urls')),  # home page
]
```

> ✅ Home page `/` → Stock Movements
> ✅ `/movements/` also accessible

---

## 2️⃣ `apps/movements/models.py`

```python
class StockMovements(models.Model):
    STATUS_CHOICES = [(1, 'Active'), (0, 'Inactive')]

    item = models.ForeignKey(StockItems, on_delete=models.DO_NOTHING)
    document_type = models.ForeignKey(StockDocType, on_delete=models.DO_NOTHING)
    document_number = models.IntegerField()
    document_reference = models.TextField(null=True, blank=True)
    quantity = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    movement_date = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'stock_movements'
        managed = False

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
```

> ✅ Auto-handles timestamps
> ✅ `managed=False` ensures Django doesn’t modify the table

---

## 3️⃣ `apps/movements/forms.py`

```python
class StockMovementsForm(forms.ModelForm):
    movement_date = forms.DateTimeField(
        initial=timezone.now,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )

    class Meta:
        model = StockMovements
        fields = [
            'item', 'document_type', 'document_number',
            'document_reference', 'quantity', 'status', 'movement_date'
        ]
        widgets = {
            'item': forms.Select(attrs={'class': 'form-select'}),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'document_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'document_reference': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
```

---

## 4️⃣ `apps/movements/views.py`

```python
@login_required
def index(request):
    records = StockMovements.objects.all().order_by('-id')
    
    # Table dropdown
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock%'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    user_group = request.user.groups.values_list('name', flat=True).first()
    
    return render(request, 'movements/index.html', {
        'title': 'Stock Movements List',
        'records': records,
        'tables': tables,
        'current_table': 'stock_movements',
        'user_group': user_group,
    })
```

*Add, Update, Delete functions* follow the same Admin-only permission logic as in UOM guide.

---

## 5️⃣ JS Table Navigation (Centralized)

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const tableSelect = document.getElementById('tableSelect');

    if (tableSelect) {
        const tableMap = {
            'stock_items_categories': '/categories/',
            'stock_document_type': '/doctype/',
            'stock_items': '/items/',
            'stock_items_uom': '/uom/',
            'stock_movements': '/'
        };

        tableSelect.addEventListener('change', function() {
            const selectedTable = this.value;
            if (tableMap[selectedTable]) {
                window.location.href = tableMap[selectedTable];
            }
        });
    }
});
```

> ✅ Modular, easy to extend for other modules

---

## 6️⃣ Templates

**`index.html`**

* Movement Date: `{{ row.movement_date|date:"d/m/Y" }}`
* Updated At: `{{ row.updated_at|date:"d M. Y, g:i a" }}`
* Admin users see Add/Update/Delete buttons; normal users see disabled buttons

**`form.html`**

* Datetime-local input for `movement_date`
* Admin-only submission

---

## 🎉 Final Result

| Feature            | Admin             | User              |
| ------------------ | ----------------- | ----------------- |
| View all movements | ✅ Yes             | ✅ Yes             |
| Add/Update/Delete  | ✅ Yes             | ❌ No              |
| Date formatting    | ✅ Yes             | ✅ Yes             |
| Table navigation   | ✅ Yes             | ✅ Yes             |
| Home page `/`      | ✅ Stock Movements | ✅ Stock Movements |

> Users can view stock movements but cannot make any changes. Admin users have full CRUD access.
