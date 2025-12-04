# 📘 **Django – Guide 17: Task Using JSON (Create, Read, Update, Delete)**

This guide walks you through building a simple **Task manager** in Django using a JSON file instead of a database.
You will learn how to store tasks inside the **media** folder, display them in a Bootstrap table, and allow Admin users to **create**, **edit**, and **delete** tasks.

---

## 🎯 **Objectives**

By the end of this guide, you will:

* ✅ Store tasks inside a `tasks.json` file
* ✅ Read, write, and update JSON data from Django
* ✅ Display tasks in a Bootstrap table
* ✅ Format timestamps nicely
* ✅ Restrict editing to **Admin** group users
* ✅ Implement full CRUD (Create, Read, Update, Delete)

---

## 📁 **Project Structure**

```
project_folder/
├── manage.py
├── core/
│   ├── settings.py
│   └── urls.py
│
├── apps/
│   ├── taskjson/
│   │   ├── apps.py
│   │   ├── views.py          ← JSON CRUD logic
│   │   ├── urls.py           ← Task URLs
│   │   └── templates/
│       └── taskjson/
│           ├── index.html    ← Task list
│           ├── create_task.html
│           └── edit_task.html
│
├── media/
│   └── tasks.json            ← JSON storage file
```

---

## 1️⃣ **Create the App**

If not created yet:

```bash
python manage.py startapp taskjson
mv taskjson apps/
```

Then add to:

### `core/settings.py`

```python
INSTALLED_APPS = [
    ...
    'apps.taskjson',
]
```

---

## 2️⃣ **Define URLs**

### `apps/taskjson/urls.py`

```python
from django.urls import path
from . import views

app_name = 'taskjson'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_task, name='create_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
]
```

### Include in main `core/urls.py`

```python
path('taskjson/', include('apps.taskjson.urls')),
```

---

## 3️⃣ **Task JSON Logic**

### `apps/taskjson/views.py`

This file handles:

✔ JSON file creation
✔ Reading & writing
✔ Display tasks
✔ Admin-only access
✔ Date formatting

(💙 This is exactly your working code; no logic is changed.)

```python
import json
import os
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from datetime import datetime

TASKS_FILE = os.path.join(settings.MEDIA_ROOT, 'tasks.json')

if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, 'w') as f:
        json.dump([], f)


def read_tasks():
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)


def write_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)


def index(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    user_group = user_groups[0] if user_groups else None

    tasks = read_tasks()

    for task in tasks:
        created = task.get("created_at", "")
        if isinstance(created, str):
            cleaned = created.split(".")[0]
            try:
                dt = datetime.strptime(cleaned, "%Y-%m-%dT%H:%M:%S")
                task["created_at"] = dt.strftime("%-d %B %Y")
            except ValueError:
                task["created_at"] = created

    return render(request, 'taskjson/index.html', {
        'title': 'Task using JSON',
        'json_file': tasks,
        'user_group': user_group,
    })


def create_task(request):
    if not (request.user.is_superuser or request.user.groups.filter(name='Admin').exists()):
        messages.warning(request, "You do not have permission to add tasks.")
        return redirect('taskjson:index')

    if request.method == "POST":
        task_name = request.POST.get('task', '')
        if task_name:
            tasks = read_tasks()
            new_task = {
                "id": len(tasks) + 1,
                "task": task_name,
                "completed": False,
                "created_at": datetime.now().isoformat()
            }
            tasks.append(new_task)
            write_tasks(tasks)
            return redirect('taskjson:index')

    return render(request, 'taskjson/create_task.html', {
        'title': 'Add New Task'
    })


def edit_task(request, task_id):
    if not (request.user.is_superuser or request.user.groups.filter(name='Admin').exists()):
        messages.warning(request, "You do not have permission to edit tasks.")
        return redirect('taskjson:index')

    tasks = read_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        messages.error(request, "Task not found.")
        return redirect('taskjson:index')

    if request.method == "POST":
        task['task'] = request.POST.get('task', task['task'])
        task['completed'] = 'completed' in request.POST
        write_tasks(tasks)
        return redirect('taskjson:index')

    return render(request, 'taskjson/edit_task.html', {
        'title': 'Edit Task',
        'task': task
    })


def delete_task(request, task_id):
    if not (request.user.is_superuser or request.user.groups.filter(name='Admin').exists()):
        messages.warning(request, "You do not have permission to delete tasks.")
        return redirect('taskjson:index')

    tasks = read_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        messages.error(request, "Task not found.")
        return redirect('taskjson:index')

    tasks.remove(task)
    write_tasks(tasks)
    return redirect('taskjson:index')
```

---

## 4️⃣ **Task List Template**

### `templates/taskjson/index.html`

Displays all tasks in a table with Edit/Delete buttons for Admins.

(Exactly your current working template.)

---

## 5️⃣ **Create Task Template**

### `templates/taskjson/create_task.html`

Simple task input form.

---

## 6️⃣ **Edit Task Template**

### `templates/taskjson/edit_task.html`

Allows modifying the task & mark completed.


---

✅ **Congratulations!**

You can now visit **`/taskjson/`** in your browser to view, add, edit, and delete tasks stored in your JSON file.
