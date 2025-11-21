Berikut **Project Requirements Document (PRD)** versi lengkap untuk **POS Café with AI-Assisted Product Creation**, ditulis dengan **format, gaya, dan detail yang sama** seperti contoh yang kamu berikan — namun sepenuhnya disesuaikan dengan proyek POS Café + AI.

---

# **Project Requirements Document: pos-cafe-ai**

---

# **1. Project Overview**

The **pos-cafe-ai** project is a modern Point-of-Sale (POS) web application designed specifically for cafés that want to streamline menu management through automation and AI assistance. It provides a fully functional baseline system that includes manual product CRUD, AI-powered product insertion, category organization, and product listings. The goal of this project is to dramatically simplify the process of adding and managing café menu items, especially when handling multiple items at once.

This system is being created to solve the common pain points café owners and staff face: manually adding dozens of products, maintaining consistent categories, and keeping stock information updated. The application integrates with an AI model to parse natural language instructions into structured product data, reducing the time needed for data entry and minimizing mistakes.

Key objectives include:

1. Providing a working POS-like product management interface,
2. Enabling AI-assisted product creation from natural language input,
3. Implementing a clean and maintainable Django backend structure,
4. Offering a Tailwind-powered frontend for clarity and usability, and
5. Using PostgreSQL for a reliable relational schema that stores product, category, and AI logs.

Success is measured by:

* Ability to add 10+ products via AI in a single instruction
* Zero JSON parsing failures when AI prompt is followed
* Under 300 ms response times for manual product CRUD
* Zero unvalidated AI data reaching the database

---

# **2. In-Scope vs. Out-of-Scope**

## **In-Scope (Version 1)**

### **Core Features**

* Manual product CRUD:

  * Add product
  * Edit product
  * List products
  * Deactivate product
* AI-assisted product creation:

  * Accept natural-language input
  * Call AI API (OpenAI or compatible)
  * Validate AI-generated items
  * Insert valid products
  * Return inserted + failed lists
* AI Logging:

  * Save raw instruction
  * Store raw AI response JSON
  * Store parsed items
  * Track status (success/partial/failed)
* Frontend pages:

  * Product list page
  * Add manual product page
  * Add product via AI page
* Tailwind CSS styling and UI layout
* Django REST API backend
* PostgreSQL database schema and migrations

## **Out-of-Scope (Future Phases)**

* Order/invoice POS system
* Authentication & user accounts
* Inventory movement & tracking
* Multi-branch (multi-outlet) capability
* Mobile-native apps
* AI product editing (only creation is included for V1)
* Product image uploads and object storage integration
* Role-based access control
* Advanced AI reasoning (e.g., price prediction, category auto-suggestion beyond simple inference)

---

# **3. User Flow**

A user lands on the main product list page, which shows all menu items. From there, the user can choose between manually adding a product or using the AI-assisted flow.

### **Manual Flow**

1. User opens the “Add Product” page.
2. They fill in fields such as name, category, price, and stock.
3. When submitting, the backend validates the data and, if correct, stores the product.
4. User is redirected back to the product list.

### **AI Flow**

1. User opens the “Add Product via AI” page.
2. They write a natural-language instruction — for example:
   *“Add iced latte 25k stock 20, caramel macchiato 28k stock 15, and almond croissant 18k stock 10.”*
3. User submits the instruction.
4. Backend saves a raw AI log entry.
5. Backend calls the AI model with a strict JSON-output prompt.
6. AI returns a structured JSON of items.
7. Backend validates each item:

   * Ensures numeric price
   * Ensures non-negative stock
   * Infers categories if missing
   * Ensures uniqueness (no duplicate product names)
8. Valid items are inserted into the database.
9. Invalid ones (e.g., missing price) are recorded in the “failed” response.
10. Frontend displays inserted + failed products.

Unauthorized access logic is not included because authentication is out-of-scope for V1.

---

# **4. Core Features**

### **Product List Page**

* Displays all products in a table
* Shows: name, category, price, stock, status
* Options: edit, deactivate

### **Manual Product Creation Page**

* Form fields: name, price, stock, category
* Client-side validation (basic)
* Backend validation (strict)
* Returns user to list after success

### **AI Product Creation Page**

* Single large textarea for instruction
* Button: “Generate from AI”
* Sends to `/api/ai/add-products/`
* Backend:

  * Logs instruction
  * Calls AI
  * Parses structured items
  * Validates and saves products
* Returns:

  * `inserted = []`
  * `failed = []`
* Displays a friendly summary of results

### **Backend AI Processing Feature**

* Central service that:

  1. Calls AI via client
  2. Parses JSON
  3. Validates fields
  4. Inserts products
  5. Logs all details

### **Backend Tables**

* `products`
* `categories`
* `ai_logs`
* `ai_parsed_items`

---

# **5. Tech Stack & Tools**

### **Frontend**

* **HTML + JavaScript** (modular)
* **Tailwind CSS** for styling
* **Fetch API** for calling backend

### **Backend**

* **Django** for API development
* **Django REST Framework** for REST endpoints
* **Python 3.x**

### **Database**

* **PostgreSQL** for relational consistency
* JSONB for AI logs

### **AI Provider**

* OpenAI (or any compatible LLM with strict JSON mode)

### **Developer Tools**

* VS Code
* Postman / Thunder Client
* Cursor / ChatGPT for assisted coding
* Python virtual environment

---

# **6. Non-Functional Requirements**

### **Performance**

* Manual CRUD API responses under 300 ms
* AI processing depends on model latency (~1–3 seconds)

### **Security**

* HTTPS in production
* Input validation on all fields
* AI output never trusted without validation
* No user authentication (intended in future version)

### **Scalability**

* Django app should run in multiple container instances
* PostgreSQL prepared for 10k+ rows of products
* AI calls can be offloaded to async workers later

### **Usability**

* Clean and readable UI
* Natural-language AI instructions
* Clear error messaging
* Mobile-friendly layouts

### **Maintainability**

* Clean app organization: `/products` and `/ai` Django apps
* Service-layer architecture
* Migrations must remain backward compatible

---

# **7. Constraints & Assumptions**

### **Constraints**

* Only English/Indonesian natural language processing supported
* AI output may vary; strict prompt engineering required
* No authentication layer in V1
* Requires stable internet connection for AI calls

### **Assumptions**

* PostgreSQL is available
* OpenAI API key is provided
* Café menu size does not exceed a few thousand products
* Single café operator (no multi-tenant complexity yet)

---

# **8. Known Issues & Potential Pitfalls**

### **AI Misinterpretation**

Natural-language instructions may produce incorrect products if phrased ambiguously.
**Mitigation**: Strict prompt enforcing JSON shape.

### **Partial Success**

Some products may fail while others succeed.
**Mitigation**: Return inserted + failed lists clearly.

### **Duplicate Product Names**

AI may generate items already in database.
**Mitigation**: Backend enforces uniqueness checks.

### **Invalid Pricing Formats**

AI may output numbers incorrectly.
**Mitigation**: Server normalizes formats and returns errors if mismatch.

### **Frontend Message Clutter**

Too many error messages could confuse users.
**Mitigation**: Use collapsible lists.

### **No Authentication**

Anyone who can access the app can modify items.
**Mitigation**: Add authentication in V2.

---

# **9. Conclusion and Summary**

The **pos-cafe-ai** project provides a solid foundation for a modern, AI-enhanced café menu management system. With manual CRUD, AI-powered product creation, structured logging, and a clean separation of backend components, this version lays the groundwork for a full POS system in future releases.

This PRD acts as the **single source of truth** for the project, guiding the development of backend, frontend, database, documentation, and overall architecture. It ensures clarity and consistency so any developer—or any AI coding assistant—can generate or modify code based on well-defined requirements.

---

Jika kamu ingin, aku bisa lanjut membuat: