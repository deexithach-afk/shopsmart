# ShopSmart – Smart Purchase Optimizer

**ShopSmart** is a modular Python-based terminal application designed to help users manage products, track shopping purchases, organize product categories, optimize spending against a budget, and generate analytical reports.

---

## 📂 Project Structure

```text
ShopSmart/
│
├── main.py            # Main application menu and loop execution
├── products.py        # Module 2, 3, 4: Add, View, Update, and Delete products
├── operations.py      # Module 5, 6: Search, Category & Price filtering, Smart Optimizer
├── reports.py         # Module 7: Analytical reports & file export
├── storage.py         # Module 8: JSON file persistence & default initialization
├── test_shopsmart.py  # Automated unit tests for all core features
│
└── products.json      # Structured database file storing product records
```

---

## 🚀 How to Run the Project

### Prerequisites
- Python 3.8 or higher installed on your computer.

### Step 1: Open Terminal in the Project Folder
Open your terminal or command prompt (PowerShell, CMD, or VS Code integrated terminal) and navigate to the project directory:
```bash
cd c:\Users\deexi_\OneDrive\Desktop\shopsmart
```

### Step 2: Run the Application

#### Option A: Interactive Terminal App (Console)
```bash
python main.py
```

#### Option B: Web Application (Localhost Dashboard)
```bash
python app.py
```
Then open your browser and navigate to:
- 🏠 **Index (Landing Page)**: [http://localhost:5000/](http://localhost:5000/)
- 🔑 **Login & Register Page**: [http://localhost:5000/login](http://localhost:5000/login)
- 📊 **Main Dashboard**: [http://localhost:5000/dashboard](http://localhost:5000/dashboard)

> **🎨 Background Color & Theme Options:**
> - Click the **"🎨 BG Color"** button in the header of any page to switch between 8 pre-designed palettes (Default Slate, Dark Mode, Emerald Mint, Ocean Blue, Warm Rose, Soft Lavender, Warm Amber, OLED Charcoal) or pick **any custom color** with the built-in color picker.
> - The theme auto-adapts text and card contrast and saves across page refreshes.

> **Demo Login Credentials:**
> - **Admin:** `admin` / `admin123`
> - **Shopper:** `shopper` / `shopper123`
> - *(Or click "Create Account" on the login page to register a new user!)*

### Step 3: Run Automated Tests
```bash
python test_shopsmart.py
```

---

## 📋 Implemented Modules & Features

### Module 1: User Menu
Displays the main menu on start and validates user input:
```
===== SHOPSMART =====
1. Add Product
2. View Products
3. Update Product
4. Delete Product
5. Search Product
6. Filter by Category
7. Generate Report
8. Exit
```

### Module 2: Add Product
- Prompts for **Product ID**, **Product Name**, **Category**, **Quantity**, and **Price**.
- **Validations**:
  - Ensures Product ID is non-empty and unique (prevents duplicate IDs).
  - Ensures Quantity is a positive integer (`> 0`).
  - Ensures Price is a positive number (`> 0`).
- Automatically persists the new product into `products.json`.

### Module 3: View Products
- Displays all registered products in a clean, aligned tabular format.
- Displays: `ID`, `Product Name`, `Category`, `Quantity`, `Price`, and `Total Value` (`Price × Quantity`).
- Calculates and displays total unique items, total item units, and overall cart total.

### Module 4: Update and Delete
- **Update**:
  - Search by Product ID.
  - Choose to update Price, Quantity, Name, Category, or both Price & Quantity.
  - Validates all modified inputs before saving.
- **Delete**:
  - Search by Product ID.
  - Asks for confirmation (`y/n`) before permanently removing the product.

### Module 5: Search and Filter
- **Search by Name**: Case-insensitive partial matching (e.g., searching `"ric"` finds `"Rice"`).
- **Filter by Category**: Lists available categories and filters products matching the selected category.
- **Filter by Price Range**: Filters products within a minimum and maximum price threshold (`min_price` to `max_price`).

### Module 6: Smart Purchase Optimization
- Calculates total purchase cost (`Quantity × Price` summed across all items).
- Identifies the **most expensive** product and **cheapest** product.
- **Budget Comparison**: Users can enter a target shopping budget.
  - Identifies if the cart is **WITHIN BUDGET** (shows remaining savings) or **BUDGET EXCEEDED** (shows deficit).
  - Detects single products that exceed the entire budget.
  - Provides smart cost-cutting recommendations based on highest expense items.

### Module 7: Generate Reports
- Displays an executive summary:
  1. Overview & Total Expenditure
  2. Price Extremes (Most expensive & cheapest)
  3. Category-Wise Spending Breakdown (Count, Units, Total Spent, % Share)
  4. Smart Budget Status
- Optional feature: Export the complete report to a text file (`shopping_report.txt`).

### Module 8: File Storage (`storage.py` & `products.json`)
- Stores records in structured JSON format.
- Automatically loads data when the application starts.
- Automatically saves data after every Add, Update, or Delete operation.
- Gracefully handles file missing or corrupted data without crashing.

---

## 🎓 Python Concepts Implemented (Faculty / Viva Reference)

| Python Concept | Where and How It Is Used in ShopSmart |
| :--- | :--- |
| **Variables** | Store product attributes (`product_id`, `name`, `price`, `quantity`), totals, and loop counters. |
| **Lists** | Store the collection of all products (`products`), search results, and category lists. |
| **Dictionaries** | Store individual product records (e.g., `{"id": "101", "name": "Rice", ...}`) and category summaries. |
| **If-else Statements** | Menu option selection, validation of non-negative prices, budget status checks (`WITHIN BUDGET` vs `EXCEEDED`). |
| **Loops (`for` & `while`)** | `while True` for the interactive menu loop; `for` loops to iterate through products and calculate totals. |
| **Functions** | Modular functions in each file (e.g., `calculate_total_cost()`, `add_product()`, `generate_report()`). |
| **File Handling** | Using `with open("products.json", ...)` with explicit `utf-8` encoding to read and write data safely. |
| **JSON Module** | Using `json.load()` and `json.dump()` with `indent=4` for structured persistence. |
| **Exception Handling** | `try-except` blocks catching `ValueError`, `FileNotFoundError`, `json.JSONDecodeError`, and `KeyboardInterrupt`. |
| **Modular Programming** | Code divided into 5 specialized modules (`main.py`, `products.py`, `operations.py`, `reports.py`, `storage.py`). |

---

## 🧪 Sample Test Run

### Initial Sample Data:
- ID `101`: Rice (Grocery, Qty: 2, ₹60.00)
- ID `102`: Shirt (Clothing, Qty: 1, ₹500.00)
- ID `103`: Milk (Grocery, Qty: 3, ₹30.00)
- ID `104`: Headphones (Electronics, Qty: 1, ₹1200.00)
- ID `105`: Apple (Grocery, Qty: 6, ₹25.00)

**Total Cart Value**: `₹2,060.00`
- If budget is set to `₹2,500.00`: Status is **WITHIN BUDGET** (Savings: `₹440.00`).
- If budget is set to `₹1,500.00`: Status is **BUDGET EXCEEDED** (Deficit: `₹560.00`), with an alert that Headphones (`₹1,200.00`) consume 58.3% of the total cart.

