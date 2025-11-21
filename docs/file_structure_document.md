Berikut **File Structure Document** lengkap untuk proyek **pos-cafe-ai**, ditulis dengan format profesional, jelas, dan siap dimasukkan ke folder `docs/`.

---

# **File Structure Document – pos-cafe-ai**

This document describes the full file and folder structure for the **pos-cafe-ai** project. It explains where every important file lives, what its purpose is, and how backend, frontend, and shared resources are organized. The structure is designed for clarity, scalability, and easy integration with AI-assisted coding tools.

---

# **1. Top-Level Project Structure**

```
pos-cafe-ai/
│
├── backend/
├── frontend/
├── docs/
│
├── README.md
└── .env.example
```

### **Description**

* **backend/** — Django + DRF backend, AI logic, database models.
* **frontend/** — HTML, JS, Tailwind CSS UI.
* **docs/** — All project documentation (PRD, guidelines, flows, etc.).
* **README.md** — Project overview & setup instructions.
* **.env.example** — Template for environment configuration.

---

# **2. Backend Folder Structure**

```
backend/
│
├── manage.py
├── requirements.txt
│
└── pos_backend/
│     ├── __init__.py
│     ├── settings.py
│     ├── urls.py
│     ├── wsgi.py
│     └── asgi.py
│
├── products/
│     ├── __init__.py
│     ├── models.py
│     ├── serializers.py
│     ├── views.py
│     ├── urls.py
│     ├── services.py
│     ├── admin.py
│     └── tests.py
│
├── ai/
│     ├── __init__.py
│     ├── models.py
│     ├── serializers.py       (optional)
│     ├── views.py
│     ├── urls.py
│     ├── services.py
│     ├── ai_client.py
│     └── tests.py
│
└── common/
      ├── __init__.py
      ├── utils.py
      ├── validators.py
      └── exceptions.py
```

---

## **2.1 pos_backend/**

Core Django project configuration.

| File                  | Description                                               |
| --------------------- | --------------------------------------------------------- |
| `settings.py`         | Django config: DB settings, installed apps, CORS, AI keys |
| `urls.py`             | Root API router → includes products & ai routes           |
| `wsgi.py` / `asgi.py` | Server entrypoints (WSGI/ASGI)                            |
| `__init__.py`         | Package initializer                                       |

---

## **2.2 products/**

Manages products and categories.

| File             | Description                                                |
| ---------------- | ---------------------------------------------------------- |
| `models.py`      | Product & Category models                                  |
| `serializers.py` | DRF serializers for product CRUD                           |
| `views.py`       | API endpoints for list/create/update/deactivate            |
| `services.py`    | Business logic (duplicate checks, product creation helper) |
| `urls.py`        | Routes under `/api/products/`                              |
| `admin.py`       | Optional Django admin integrations                         |
| `tests.py`       | Unit tests for product features                            |

---

## **2.3 ai/**

Handles AI-assisted product creation & logs.

| File             | Description                                                 |
| ---------------- | ----------------------------------------------------------- |
| `models.py`      | AiLog & AiParsedItem models                                 |
| `ai_client.py`   | Code to call OpenAI API                                     |
| `services.py`    | Core logic: validate AI response, insert items, create logs |
| `views.py`       | Endpoint: `/api/ai/add-products/` & `/api/ai/logs/`         |
| `urls.py`        | AI route definitions                                        |
| `serializers.py` | Optional serializers for logs                               |
| `tests.py`       | Test coverage for AI logic                                  |

---

## **2.4 common/**

Reusable shared “library” code.

| File            | Description                                            |
| --------------- | ------------------------------------------------------ |
| `utils.py`      | Helpers (price normalization, string processing, etc.) |
| `validators.py` | Central validation functions                           |
| `exceptions.py` | Custom error types used across apps                    |

---

# **3. Frontend Folder Structure**

```
frontend/
│
├── public/
│     └── index.html
│
└── src/
      ├── css/
      │     ├── tailwind.css
      │     └── components.css
      │
      └── js/
            ├── api.js
            ├── products-page.js
            ├── add-product-page.js
            ├── add-product-ai-page.js
            └── ui-helpers.js
│
├── tailwind.config.js
├── postcss.config.js
└── package.json
```

---

## **3.1 public/**

Static HTML files.

| File         | Description                               |
| ------------ | ----------------------------------------- |
| `index.html` | Landing page or redirect to products.html |

---

## **3.2 src/css/**

Tailwind styling and additional UI CSS.

| File             | Description                                                |
| ---------------- | ---------------------------------------------------------- |
| `tailwind.css`   | Tailwind entryfile (`@tailwind base/components/utilities`) |
| `components.css` | Optional custom styles                                     |

---

## **3.3 src/js/**

All frontend logic, divided by page.

| File                     | Description                                      |
| ------------------------ | ------------------------------------------------ |
| `api.js`                 | API helper functions (GET/POST to backend)       |
| `products-page.js`       | Fetch + render product list                      |
| `add-product-page.js`    | Manual product creation logic                    |
| `add-product-ai-page.js` | AI input submission & results handling           |
| `ui-helpers.js`          | Toasts, alerts, loaders, and reusable UI helpers |

---

# **4. Docs Folder Structure**

```
docs/
│
├── app_summary.md
├── app_flow_document.md
├── app_flowchart.md
├── backend_structure_document.md
├── frontend_guidelines_document.md
├── project_requirements_document.md
├── security_guidelines_document.md
└── tech_stack_document.md
```

Each file serves as a knowledge base for the project and can be consumed by AI coding assistants (Cursor, ChatGPT, etc.) during code generation.

---

# **5. Environment & Config Files**

| File           | Purpose                                          |
| -------------- | ------------------------------------------------ |
| `.env.example` | Template for environment variables (DB, AI keys) |
| `README.md`    | Installation instructions, tech overview         |

---

# **6. Summary**

This structure ensures the project is:

* **Modular** (AI logic isolated from product logic)
* **Maintainable** (clear separation of frontend, backend, docs)
* **AI-friendly** (services and utilities cleanly isolated)
* **Scalable** (easy to add auth, orders, invoices later)
* **Beginner-friendly** (no complicated dependencies)

This is the recommended file structure for a clean, production-ready POS application integrating AI.

---