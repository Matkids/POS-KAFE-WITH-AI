Berikut **App Flow Document** versi **bahasa Inggris**, ditulis dengan format naratif seperti contoh template yang kamu berikan.

---

# **App Flow Document – POS Café with AI-Assisted Product Creation**

## **Opening the Application & First Interaction**

When a user visits the application’s root URL, they are greeted with a simple landing page that provides two main actions: viewing existing products or adding new ones. Since this version of the application does not include authentication, users can immediately begin managing products without signing up or logging in.

If the user chooses to view products, the app loads a table of all existing menu items. This list includes product name, category, price, stock, and active status. The frontend retrieves this data by sending a request to the backend’s product API, and the table refreshes automatically whenever changes occur.

Navigation options at the top or side of the page allow users to move between sections such as “Add Product Manually” or “Add Products via AI,” ensuring the workflow is intuitive and accessible.

---

## **Adding Products Manually**

When the user clicks **“Add Product Manually,”** they are brought to a page or modal containing a simple form. The fields include:

* Product name
* Product category
* Price
* Initial stock

After filling in the form, the user clicks **Save**, triggering a `POST` request to the backend API. The backend performs validation:

* Price must be a valid integer
* Stock cannot be negative
* Name cannot be empty
* Category must be valid

If validation fails, the form reappears with clear inline error messages.
If the data is valid, the new product is saved to the database, and the user is returned to the product list with the newly added item visible.

---

## **Adding Products via AI (Natural Language Input)**

This feature is the most innovative part of the application.

When users navigate to **“Add Products via AI,”** they see a dedicated section with a single large text area where they can write natural-language instructions such as:

> “Add iced coffee 22k stock 30, hot latte 25k stock 15, and chocolate croissant 18k stock 20.”

After writing the instruction, they click **Generate from AI**.

The following process occurs:

1. The frontend sends the instruction to the backend using `POST /api/ai/add-products/`.
2. The backend creates an initial AI log entry containing the raw instruction.
3. The backend calls the AI service using a strict system prompt that ensures the AI returns structured JSON.
4. Once the AI responds:

   * If the response is not valid JSON, the backend marks the log as “failed” and returns an error message.
   * If the response is valid JSON, the backend continues processing.
5. The backend validates each item in the AI-generated `items` array:

   * Product name must be present
   * Price must be a valid integer
   * Stock must be ≥ 0
   * Category may be inferred if not explicitly stated
   * Duplicate product names must be rejected
6. For each item:

   * Valid items are inserted into the `products` table.
   * Invalid items are recorded as “failed” with an explanation.
7. Each AI-parsed item is recorded in the `ai_parsed_items` table for auditing.
8. The backend returns a response containing:

   * `inserted`: successfully saved products
   * `failed`: invalid products with failure reasons
9. The frontend displays a clear summary showing which products were added and which failed.

The user can return to the product list to view all newly added items without reloading the page.

---

## **Editing Existing Products**

Each row in the product list includes an **Edit** button.

When clicked:

1. The user is taken to a pre-filled edit form.
2. They adjust the fields as needed.
3. They click **Save**, triggering a `PUT /api/products/{id}/` request.
4. The backend validates and updates the product.
5. The frontend updates the table immediately to reflect the changes.

---

## **Deactivating or Removing Products**

Products can be “removed” using soft deletion:

1. The user clicks **Deactivate** beside a product.
2. A confirmation dialog appears.
3. After confirming, the frontend sends a `PATCH /api/products/{id}/` request with `{ "is_active": false }`.
4. The backend updates the product’s status.
5. The product list refreshes to show the updated state.

This approach preserves historical data while hiding inactive menu items.

---

## **Viewing AI Logs (Optional Feature for Admins/Developers)**

For auditing and debugging, the application can display a full history of AI interactions.

1. The user navigates to **AI Logs**.
2. Frontend sends `GET /api/ai/logs/`.
3. Backend returns a list of logs containing:

   * Timestamp
   * Raw instruction
   * Status (success, partial, failed)
4. Clicking a log entry triggers `GET /api/ai/logs/{id}/`.
5. Backend returns:

   * Full AI response
   * Parsed items
   * Inserted and failed items
   * Error messages if applicable

This allows developers to identify problems with AI processing or refine prompts.

---

## **Error States and Alternate Paths**

### **Invalid AI Output**

If the AI response cannot be parsed as JSON:

* The backend marks the log as failed.
* A clear error message is returned.
* The frontend notifies the user to adjust their instruction.

### **Partial Success**

If some items cannot be inserted:

* Valid items are saved.
* Invalid ones appear in the `failed` list with detailed reasons.
* The log is marked as “partial.”

### **Empty Result**

If AI returns zero items:

* Backend sends a message like:
  *“No products detected from your instruction.”*
* User can adjust and try again.

### **Network or Backend Failures**

In the event of API or connectivity issues:

* UI displays a generic error message.
* Logs still capture the request for later inspection.

---

## **Conclusion & Overall App Journey**

A typical user experience flows smoothly from landing on the welcome page to managing a full café menu.
The AI-assisted product creation dramatically accelerates workflow by allowing users to add multiple products with a single instruction, while still ensuring correctness through backend validation and auditing.

Users can manually edit or deactivate products, review AI logs, and navigate across the dashboard without authentication barriers.
Every step provides clear communication in case of errors, ensuring reliability and ease of use.

This application foundation is designed to grow into a fully featured POS system with inventory management, order handling, and analytics in future releases.

---
