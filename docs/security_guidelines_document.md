Berikut **Security Guidelines Document** untuk **POS Café with AI-Assisted Product Creation**, ditulis **mengikuti format, struktur, gaya, dan kedalaman** yang sama seperti contoh yang kamu berikan.

---

# **Security Guidelines for pos-cafe-ai**

This document defines mandatory security principles and implementation best practices tailored specifically to the **pos-cafe-ai** repository. It aligns with Security-by-Design, Least Privilege, Defense-in-Depth, and other core security tenets. All sections reference relevant backend components (Django REST API, AI service integration, environment variables, database configuration) to ensure practical, actionable guidance.

---

# **1. Security by Design**

* Integrate security considerations **from day one** across all features—manual product insertion, AI-assisted product creation, and product listing.
* Conduct a brief **threat review** whenever adding new API endpoints (e.g., new `/api/products/` routes).
* Keep Django’s `DEBUG = False` in staging/production environments.
* Enforce “secure defaults”:

  * Disable verbose error messages in production
  * Enable SSL redirection if hosting environment supports it
* Maintain a **Security Checklist** in all pull requests ensuring the contributor has reviewed:

  * Input validation
  * API permissions (even if using public endpoints)
  * Proper handling of AI responses

---

# **2. Authentication & Access Control (Future Expansion)**

Although Version 1 ships without authentication, these guidelines prepare the project for future secure scaling.

## **2.1 Password Storage**

* When authentication is added later:

  * Store hashed passwords using **bcrypt** or **Argon2** (Django has built-in Argon2 support).
  * Enforce strong password policies:
    Minimum 12 characters, mix of uppercase/lowercase, numbers, and symbols.

## **2.2 Session Management**

* Use Secure, HttpOnly, SameSite=Strict cookies.
* Prevent exposure of session tokens to JavaScript.
* Regenerate session IDs on login to prevent session fixation.
* Set idle timeouts (e.g., auto-expire after 30 minutes of inactivity).

## **2.3 Rate Limiting**

* Even without login logic, apply throttling to:

  * AI generation endpoint `/api/ai/add-products/`
  * Product creation endpoints
* Use Django REST Framework’s throttling classes or middleware.

## **2.4 Role-Based Access Control (Future)**

* Implement roles (e.g., admin, staff).
* Apply permission checks on:

  * Product creation
  * Product deletion/deactivation
  * AI log viewing

---

# **3. Input Handling & Processing**

## **3.1 Validate & Sanitize All Inputs**

* All user and AI inputs **must be revalidated** server-side, even if client-side validation exists.
* Use DRF serializers to validate:

  * Name length
  * Stock integer rules
  * Price numeric rules
  * Category validity
* Reject any unexpected or additional fields.

## **3.2 Prevent Injection**

* Django ORM prevents SQL injection if used properly.
* Never use raw SQL unless parameterized.
* Do not trust AI output—validate every field using strict types.
* Avoid dynamic evaluation of AI responses.

## **3.3 Safe Redirects**

* If future redirect logic is introduced, restrict allowed redirect URLs to prevent open redirect attacks.

---

# **4. Data Protection & Privacy**

## **4.1 Encryption & Secrets**

* Enforce HTTPS/TLS for all client → backend → AI provider communication.
* Store secrets using environment variables:

  * `OPENAI_API_KEY`
  * Database credentials
  * Django `SECRET_KEY`
* Never commit secrets to version control.

## **4.2 Sensitive Data Handling**

* Never log:

  * Raw passwords (for future auth)
  * AI API keys
  * Database credentials
* AI logs may contain user instructions—treat logs as sensitive.
* Limit exposure of AI logs to authorized users only.

---

# **5. API & Service Security**

## **5.1 HTTPS Enforcement**

* Ensure production hosting forces HTTPS.
* Use Django’s `SECURE_SSL_REDIRECT=True` when deployed behind SSL.

## **5.2 CORS**

* Restrict allowed origins in Django CORS settings.
* Avoid wildcard (`*`) origins except in local development.

## **5.3 Minimal API Exposure**

* Group APIs under `/api/products/` and `/api/ai/`.
* Return only necessary fields—avoid leaking:

  * Database schema
  * Stack traces
  * Internal errors
* Use a custom error handler to standardize JSON error messages.

## **5.4 AI Service Hardening**

* Validate that AI returns JSON before parsing.
* Set strict system prompt—**never allow AI to execute dynamic code**.
* Use timeouts on AI requests to avoid resource exhaustion.

---

# **6. Web Application Security Hygiene**

## **6.1 CSRF Protection**

* Enable Django’s built-in CSRF protection for all state-changing endpoints.
* For API-only clients, use token-based CSRF headers.

## **6.2 Security Headers**

Configure Django to send:

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self';
```

## **6.3 Secure Cookies**

* Use `Secure`, `HttpOnly`, `SameSite=Strict` for any session or CSRF cookies.
* Never store tokens in localStorage.

## **6.4 Prevent XSS**

* Escape all user-provided content before rendering.
* Avoid injecting AI responses directly into HTML unless sanitized.
* Tailwind’s utility-first design reduces custom HTML injection points.

---

# **7. Infrastructure & Configuration Management**

## **Server Hardening**

* Disable debug mode in production.
* Use firewall rules to restrict incoming traffic.
* Ensure admin panels (if added later) are protected via login + IP allowlist.

## **Secret Rotation**

* Rotate:

  * Django SECRET_KEY
  * API keys (OpenAI)
  * Database passwords

## **Least Privilege**

* Database users should only have:

  * Read/write access to required tables
  * No superuser permissions
  * No schema-altering permissions from the application layer

## **Updates & Patch Management**

* Keep Python, Django, and DRF versions current.
* Apply security patches promptly.

---

# **8. Dependency Management**

* Use a `requirements.txt` or `pyproject.toml` lockfile to maintain reproducible builds.
* Audit dependencies regularly (`pip-audit`, GitHub Dependabot).
* Remove unused packages to reduce attack surface.
* Prefer well-established libraries with active maintenance.

---

# **Conclusion**

By following these security guidelines, the **pos-cafe-ai** application remains resilient, safe, and production-ready. These principles ensure the protection of user data, reliable AI interactions, and strong foundational security for future expansions, such as authentication, multi-user roles, or full POS workflows.

This document should be revisited during each feature milestone to ensure continued adherence to best practices and evolving security standards.

---