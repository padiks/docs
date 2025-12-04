# Django Modular Project

**Django Modular Project** is a lightweight, modular **Django** application demonstrating complete **CRUD** operations with **SQLite**.
It is designed as a **step-by-step learning project**, showing how to build scalable Django apps with a clean, modular architecture.

* **Sample database:** `db.sqlite3` with preloaded tables and test data.
* **Login credentials:**

  * User: `user` / `demo`
  * Admin: `admin` / `root`
* **Live demo:** [https://padiks.pythonanywhere.com](https://padiks.pythonanywhere.com)

---

## Project Highlights

* Modular Django architecture with reusable apps
* Full CRUD operations using Django ORM
* Foreign key relationships (Items → UOM)
* Role-based authentication and admin access
* Integrated Bootstrap UI with templates and partials
* Debug toolbar included
* Easy to extend and scale with new modules

---

## Structure

```
project_folder/
├── manage.py
├── core/         # settings & URL configuration
├── apps/         # modular apps (items, users, etc.)
├── templates/    # global templates
├── static/       # CSS, images
└── db.sqlite3    # sample database
```

---

## Learning Guides

16 step-by-step guides covering:

* Base template & Bootstrap layout
* SQLite setup and CRUD operations
* Multi-table includes & foreign keys
* Authentication & role-based admin
* DRF API setup & REST API consumption
* Excel and PDF integration

Each guide is **fully working** and builds on the previous one.

---

## Running the Project

1. Install dependencies: `pip install -r requirements.txt`
2. Start server: `python manage.py runserver`
3. Access at `http://127.0.0.1:8000/`

No migrations are required for the included database.

---

**License:** Educational use; free to explore, extend, and learn.
