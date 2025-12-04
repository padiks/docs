# 📘 **Django – Guide 16: PDF Viewer (Page-by-Page with Buttons)**

This guide walks you through setting up a **Django** application to **load and display PDF files** inside a Bootstrap card.
You will learn how to prepare the project structure, load a PDF from the **media** folder, and render it **page-by-page** using **PDF.js**, with **Previous / Next buttons** for navigation.

---

## 🎯 **Objectives**

By the end of this guide, you will:

* ✅ Set up a Django app to display PDF files
* ✅ Store PDF files inside the **media** folder
* ✅ Serve media URLs using Django settings
* ✅ Render a **page-by-page PDF viewer** in a Bootstrap card
* ✅ Include **Previous / Next buttons** for navigation

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
│   ├── pdfview/                 ← App for PDF viewing
│   │   ├── apps.py
│   │   ├── views.py             ← Page-by-page rendering logic
│   │   └── urls.py              ← App URLs
│
├── media/
│   └── README.pdf               ← PDF file to display
```

---

## 1️⃣ **Create the PDF View App**

If you haven’t created it yet:

```bash
python manage.py startapp pdfview
mv pdfview apps/
```

Add the app to **core/settings.py**:

```python
INSTALLED_APPS = [
    ...,
    'apps.pdfview',
]
```

---

## 2️⃣ **Add Media Settings**

In **core/settings.py**, add:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## 3️⃣ **Serve Media in URLs**

In **core/urls.py**, add:

```python
from django.conf import settings
from django.conf.urls.static import static
```

At the bottom:

```python
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 4️⃣ **App URLs**

Create **apps/pdfview/urls.py**:

```python
from django.urls import path
from . import views

app_name = 'pdfview'

urlpatterns = [
    path('', views.index, name='index'),
]
```

---

## 5️⃣ **Views**

In **apps/pdfview/views.py**:

```python
from django.shortcuts import render

def index(request):
    return render(request, 'pdfview/index.html', {
        'title': 'PDF Viewer',
        'pdf_url': '/media/README.pdf',  # PDF location
    })
```

---

## 6️⃣ **Template**

Create **apps/pdfview/templates/pdfview/index.html**:

```html
{% extends 'base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="card shadow-lg p-4 mb-3 mx-auto" style="max-width: 900px;">
    <h4 class="mb-4 text-center">{{ title }}</h4>

    <!-- Navigation -->
    <div class="d-flex justify-content-between mb-3">
        <button id="prev" class="btn btn-primary btn-sm">Previous</button>
        <span>Page: <span id="page_num"></span> / <span id="page_count"></span></span>
        <button id="next" class="btn btn-primary btn-sm">Next</button>
    </div>

    <!-- PDF Canvas -->
    <div class="text-center">
        <canvas id="pdf_render" class="border w-100"></canvas>
    </div>
</div>

<!-- PDF.js CDN -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>

<script>
const url = "{{ pdf_url }}";

let pdfDoc = null,
    pageNum = 1,
    pageIsRendering = false,
    pageNumPending = null;

const scale = 1.2;
const canvas = document.querySelector("#pdf_render");
const ctx = canvas.getContext("2d");

// Render the page
const renderPage = num => {
    pageIsRendering = true;

    pdfDoc.getPage(num).then(page => {
        const viewport = page.getViewport({ scale });
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        const renderCtx = { canvasContext: ctx, viewport };
        page.render(renderCtx).promise.then(() => {
            pageIsRendering = false;
            if (pageNumPending !== null) {
                renderPage(pageNumPending);
                pageNumPending = null;
            }
        });

        document.querySelector("#page_num").textContent = num;
    });
};

// Queue render
const queueRenderPage = num => {
    if (pageIsRendering) {
        pageNumPending = num;
    } else {
        renderPage(num);
    }
};

// Previous / Next buttons
document.querySelector("#prev").addEventListener("click", () => {
    if (pageNum <= 1) return;
    pageNum--;
    queueRenderPage(pageNum);
});

document.querySelector("#next").addEventListener("click", () => {
    if (pageNum >= pdfDoc.numPages) return;
    pageNum++;
    queueRenderPage(pageNum);
});

// Load PDF
pdfjsLib.getDocument(url).promise.then(pdfDoc_ => {
    pdfDoc = pdfDoc_;
    document.querySelector("#page_count").textContent = pdfDoc.numPages;
    renderPage(pageNum);
});
</script>
{% endblock %}
```

---

## 7️⃣ **Add the URL to the Project**

In **core/urls.py**:

```python
path('pdfview/', include('apps.pdfview.urls')),
```

---

## 🎉 **Done!**

You now have a **page-by-page PDF viewer**:

* Loads PDFs from `/media/`
* Displays inside a **Bootstrap card**
* **Previous / Next buttons** work
* Ready for **flip animations** or zoom features in future guides
