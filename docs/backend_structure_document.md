Berikut **Backend Structure Document** yang ditulis **dengan gaya, format, dan kedalaman yang sama** seperti contoh yang kamu berikan—namun disesuaikan sepenuhnya untuk **POS Café dengan fitur AI-Assisted Product Creation**.

---

# **Backend Structure Document – POS Café with AI-Assisted Product Creation**

This document outlines the backend architecture, hosting considerations, and infrastructure for the POS Café application. It is written in clear, accessible language so that anyone—developers, PMs, or system designers—can understand how the backend works and how it supports AI-powered product creation.

---

# **1. Backend Architecture**

## **Framework and Design Pattern**

The backend is built using **Django** and **Django REST Framework (DRF)**.
This provides a reliable and well-structured environment for creating RESTful APIs.

The backend follows a layered architecture:

### **API Layer**

* Implemented with **DRF ViewSets or APIViews**
* Handles incoming HTTP requests such as:

  * Creating a product
  * Fetching the product list
  * Submitting natural-language instructions to AI
  * Retrieving AI logs

### **Service Layer**

* Contains business logic independent of HTTP concerns.
* Responsible for:

  * Validating AI-generated items
  * Processing AI instruction → JSON conversion
  * Coordinating inserts into multiple tables
  * Maintaining clean separation between views and core logic

### **Data Access Layer**

* Implemented via Django ORM models.
* Manages:

  * Product storage (products table)
  * Category mapping
  * AI logs and parsed records
  * Querying, filtering, pagination

This separation ensures clarity, easier debugging, and long-term maintainability.

---

## **Scalability**

* Django is stateless, so API instances can be scaled horizontally.
* The AI processing is synchronous but can later be offloaded to:

  * Celery task queues
  * Background workers
* Database queries scale well under PostgreSQL.
* Future enhancements can add:

  * Redis caching
  * Load balancing
  * Distributed AI workers

---

## **Maintainability**

* Each app (`products`, `ai`) contains isolated domain logic.
* Service modules (`services.py`) ensure DRY and reusable code.
* Strict validation rules prevent bad data from entering the database.
* Logging of AI responses makes debugging easier.

---

## **Performance**

* Django ORM reduces boilerplate and optimizes queries.
* AI parsing happens through a single request-response cycle.
* The most time-consuming operation is the AI API request.
* Future optimization:

  * AI batching
  * Async API calls
  * Caching results for repeated instructions

---

# **2. Database Management**

## **Database Choice**

The backend uses **PostgreSQL**, chosen for:

* Reliable ACID transactions
* Strong support for `JSONB` fields (ideal for AI logs)
* Structured schema for products and relations
* Scalability and indexing features

Redis may optionally be added later for faster read access or caching.

---

## **Data Storage and Access**

* Django ORM maps Python objects → PostgreSQL tables.
* Models represent:

  * Products
  * Categories
  * AI logs
  * AI parsed items
* QuerySets enable efficient filtering and updates.
* Migrations track every schema change and ensure consistent environments across dev/staging/production.

---

## **Data Practices**

* All AI-generated data is **validated server-side**.
* No data from AI is trusted without checks.
* Input from users and AI is sanitized to avoid injection attacks.
* Logs store full responses for transparency.

---

# **3. Database Schema**

## **Human-Readable Format**

### **Products Table**

* `id`: Unique product identifier
* `name`: Product name
* `category_id`: Foreign key to categories
* `price`: Integer price (rupiah)
* `stock`: Current stock
* `sku`: Optional product code
* `is_active`: Soft delete flag
* `created_at`: Timestamp
* `updated_at`: Timestamp

### **Categories Table**

* `id`: Unique identifier
* `name`: Category name (e.g., Minuman)
* `description`: Optional description

### **AI Logs Table**

* `id`: Unique log record
* `raw_instruction`: User input
* `ai_response`: Entire AI output
* `ai_model`: Model used
* `status`: success / partial / failed
* `error_message`: Optional
* `created_at`: Timestamp

### **AI Parsed Items Table**

* `id`: Unique identifier
* `ai_log_id`: Parent log id
* `name`: Parsed name
* `category`: Parsed category
* `price`: Parsed price
* `stock`: Parsed stock
* `status`: pending / inserted / failed
* `product_id`: Linked product if inserted

---

## **SQL Schema (PostgreSQL)**

```sql
-- Categories table
CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Products table
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  category_id INT REFERENCES categories(id),
  price INT NOT NULL,
  stock INT DEFAULT 0,
  sku VARCHAR(50),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- AI Logs table
CREATE TABLE ai_logs (
  id SERIAL PRIMARY KEY,
  raw_instruction TEXT NOT NULL,
  ai_model VARCHAR(100),
  ai_request JSONB,
  ai_response JSONB,
  status VARCHAR(50),
  error_message TEXT,
  created_by_id INT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- AI Parsed Items
CREATE TABLE ai_parsed_items (
  id SERIAL PRIMARY KEY,
  ai_log_id INT REFERENCES ai_logs(id) ON DELETE CASCADE,
  name VARCHAR(255),
  category VARCHAR(100),
  price INT,
  stock INT,
  status VARCHAR(50),
  product_id INT REFERENCES products(id),
  error_message TEXT
);
```

---

# **4. API Design and Endpoints**

We follow a RESTful approach centered around predictable, consistent endpoints.

---

## **Product APIs**

### `GET /api/products/`

Returns list of all products.

### `POST /api/products/`

Creates a manual product.

### `GET /api/products/{id}/`

Fetch product details.

### `PUT /api/products/{id}/`

Update full product object.

### `PATCH /api/products/{id}/`

Partial update (e.g., deactivate).

---

## **AI Endpoints**

### `POST /api/ai/add-products/`

* Accepts natural language instruction.
* Calls AI service.
* Parses output → inserts valid products.
* Returns:

  * `inserted` list
  * `failed` list
  * Logs the entire process.

### `GET /api/ai/logs/`

Returns list of AI logs.

### `GET /api/ai/logs/{id}/`

Returns full detail of one AI log.

---

## **Communication Rules**

* Frontend communicates using JSON.
* Backend sends:

  * Proper HTTP status codes
  * Detailed validation messages
  * Safe error descriptions

---

# **5. Hosting Solutions**

## Recommended Cloud Providers

* **Railway**, **Render**, **Fly.io**, or **DigitalOcean**
* Django runs under **Gunicorn** or **Uvicorn (ASGI)**

Key hosting benefits:

* Scalability through multiple instances
* Automatic restarts
* Database hosting integrated
* Environment variables for secrets

---

# **6. Infrastructure Components**

### **Load Balancer**

* Provided by hosting provider
* Distributes traffic across running Django instances

### **CDN**

* Used for static files if served via CDN (CSS/JS)
* Tailwind files can be cached globally

### **Caching**

(Optional)

* Redis for caching product lists
* Redis for caching AI responses

### **Storage**

* PostgreSQL for structured data
* S3/Spaces for file storage if needed later

### **Message Queue**

(Optional future addition)

* Celery + Redis/RabbitMQ for async AI processing

---

# **7. Security Measures**

### **Input Validation**

* Django REST Framework serializers validate all incoming data
* AI output revalidated to prevent malformed data

### **Transport Security**

* All API calls served via HTTPS
* TLS encryption ensures backend and DB connectivity is secure

### **Database Safety**

* No raw SQL
* ORM protects against SQL injection

### **CORS & CSRF**

* CORS configured to limit origins
* CSRF used for protected browser requests
* API token or cookie approach for future authentication

---

# **8. Monitoring and Maintenance**

### **Monitoring**

* Sentry for error tracking
* Prometheus/Grafana for metrics (optional)
* App logs stored in hosting provider logging

### **Logging**

* All AI interactions logged
* Structured JSON logs recommended

### **Health Checks**

* A `/health` endpoint returns 200 status if app and DB are reachable

### **Maintenance**

* Automated migrations
* Scheduled DB backups
* Dependency security audits

---

# **9. Conclusion and Backend Summary**

The POS Café backend is built with Django and DRF, providing a robust, scalable, and clear architecture. It integrates seamlessly with AI services for natural-language product creation, while ensuring all data is validated, logged, and handled securely. PostgreSQL provides reliable structured storage, and optional infrastructure enhancements like Redis, Celery, and CDN support future expansion.

This backend architecture is designed to be maintainable, scalable, and secure—and ready to grow into a full POS ecosystem as new features are added.

---