"""
operations.py - Search, Filtering, and Smart Optimization Operations

Contains functions for:
- Search products by name
- Filter products by category
- Filter products by price range
- Smart Purchase Optimization:
  * Total purchase cost calculation
  * Most expensive and cheapest products
  * Total shopping budget comparison
  * Identifying products that exceed the budget
  * Smart cost optimization recommendations
"""

import sys
from products import display_products_table, CURRENCY

# Ensure UTF-8 output encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ==========================================
# SEARCH AND FILTER FUNCTIONS (Module 5)
# ==========================================

def search_by_name(products, query):
    """
    Search products matching query in their name (case-insensitive).
    """
    query_lower = query.strip().lower()
    if not query_lower:
        return []
    return [p for p in products if query_lower in p.get("name", "").lower()]


def filter_by_category(products, category_name):
    """
    Filter products by category (case-insensitive exact match).
    """
    target = category_name.strip().lower()
    return [p for p in products if p.get("category", "").lower() == target]


def filter_by_price_range(products, min_price, max_price):
    """
    Filter products within [min_price, max_price] inclusive.
    """
    return [p for p in products if min_price <= float(p.get("price", 0.0)) <= max_price]


def get_unique_categories(products):
    """
    Return a sorted list of unique category names from the products.
    """
    categories = set()
    for p in products:
        cat = p.get("category")
        if cat:
            categories.add(cat)
    return sorted(list(categories))


# ========================================================
# SMART PURCHASE OPTIMIZATION CALCULATIONS (Module 6)
# ========================================================

def calculate_total_cost(products):
    """
    Calculate the total cost of all products (Quantity * Price).
    """
    total = 0.0
    for p in products:
        total += int(p.get("quantity", 0)) * float(p.get("price", 0.0))
    return round(total, 2)


def calculate_total_quantity(products):
    """
    Calculate the total number of individual items across all products.
    """
    return sum(int(p.get("quantity", 0)) for p in products)


def find_most_expensive_product(products):
    """
    Find product with the highest unit price.
    """
    if not products:
        return None
    return max(products, key=lambda p: float(p.get("price", 0.0)))


def find_cheapest_product(products):
    """
    Find product with the lowest unit price.
    """
    if not products:
        return None
    return min(products, key=lambda p: float(p.get("price", 0.0)))


def find_highest_spending_product(products):
    """
    Find product with the highest total expenditure (Quantity * Price).
    """
    if not products:
        return None
    return max(products, key=lambda p: int(p.get("quantity", 0)) * float(p.get("price", 0.0)))


def calculate_category_spending(products):
    """
    Group spending by category.
    
    Returns:
        dict: {
            category_name: {
                'count': int,
                'quantity': int,
                'total_cost': float,
                'percentage': float
            }
        }
    """
    summary = {}
    grand_total = calculate_total_cost(products)

    for p in products:
        cat = p.get("category", "General")
        qty = int(p.get("quantity", 0))
        price = float(p.get("price", 0.0))
        item_cost = qty * price

        if cat not in summary:
            summary[cat] = {"count": 0, "quantity": 0, "total_cost": 0.0, "percentage": 0.0}

        summary[cat]["count"] += 1
        summary[cat]["quantity"] += qty
        summary[cat]["total_cost"] += item_cost

    # Calculate percentage for each category
    if grand_total > 0:
        for cat in summary:
            summary[cat]["percentage"] = round((summary[cat]["total_cost"] / grand_total) * 100, 2)
            summary[cat]["total_cost"] = round(summary[cat]["total_cost"], 2)

    return summary


def analyze_budget(products, budget):
    """
    Perform smart optimization analysis against a user's budget.
    
    Args:
        products (list): Current products in the shopping list.
        budget (float): The total budget allocated by user.
        
    Returns:
        dict: Detailed budget analysis including difference, status,
              and products exceeding the budget.
    """
    total_cost = calculate_total_cost(products)
    diff = budget - total_cost
    is_within = diff >= 0
    percent_used = (total_cost / budget * 100) if budget > 0 else 0.0

    # Products whose individual total cost exceeds budget
    exceeding_items = []
    for p in products:
        item_cost = int(p.get("quantity", 0)) * float(p.get("price", 0.0))
        if item_cost > budget:
            exceeding_items.append({
                "product": p,
                "item_cost": item_cost,
                "excess": item_cost - budget
            })

    # Optimization suggestions: Sort products by total cost descending
    sorted_by_cost = sorted(
        products,
        key=lambda p: int(p.get("quantity", 0)) * float(p.get("price", 0.0)),
        reverse=True
    )

    return {
        "budget": round(budget, 2),
        "total_cost": total_cost,
        "difference": round(abs(diff), 2),
        "is_within_budget": is_within,
        "percentage_used": round(percent_used, 2),
        "exceeding_items": exceeding_items,
        "sorted_by_cost": sorted_by_cost
    }


# ==========================================
# INTERACTIVE USER FLOWS
# ==========================================

def search_product_flow(products):
    """
    Menu Flow for Search Product.
    Allows searching by Name or Filtering by Price Range.
    """
    print("\n----- SEARCH & FILTER PRODUCTS -----")
    if not products:
        print("[Notice] Inventory is empty. No products to search.")
        return

    print("1. Search by Product Name")
    print("2. Filter by Price Range")
    print("3. Back to Main Menu")

    choice = input("Enter choice (1-3) [Default 1]: ").strip()
    if choice == "" or choice == "1":
        query = input("Enter product name or keyword to search: ").strip()
        if not query:
            print("[Notice] Search query was empty.")
            return
        results = search_by_name(products, query)
        display_products_table(results, title=f"SEARCH RESULTS FOR '{query}'")

    elif choice == "2":
        try:
            min_p = float(input(f"Enter Minimum Price ({CURRENCY}): ").strip())
            max_p = float(input(f"Enter Maximum Price ({CURRENCY}): ").strip())
            if min_p < 0 or max_p < 0:
                print("[Error] Prices must be non-negative.")
                return
            if min_p > max_p:
                print("[Error] Minimum price cannot exceed Maximum price.")
                return
            results = filter_by_price_range(products, min_p, max_p)
            display_products_table(results, title=f"PRODUCTS PRICED {CURRENCY}{min_p:.2f} - {CURRENCY}{max_p:.2f}")
        except ValueError:
            print("[Error] Invalid price format. Please enter numeric values.")

    elif choice == "3":
        return
    else:
        print("[Error] Invalid selection.")


def filter_category_flow(products):
    """
    Menu Flow for Filtering by Category.
    """
    print("\n----- FILTER BY CATEGORY -----")
    if not products:
        print("[Notice] Inventory is empty. No products available.")
        return

    categories = get_unique_categories(products)
    if not categories:
        print("[Notice] No categories found.")
        return

    print("Available Categories:")
    for idx, cat in enumerate(categories, 1):
        cat_count = len(filter_by_category(products, cat))
        print(f"  {idx}. {cat} ({cat_count} item{'s' if cat_count != 1 else ''})")

    user_input = input("\nEnter category name or number: ").strip()
    selected_category = ""

    if user_input.isdigit():
        cat_idx = int(user_input) - 1
        if 0 <= cat_idx < len(categories):
            selected_category = categories[cat_idx]
        else:
            print("[Error] Category number out of range.")
            return
    else:
        selected_category = user_input

    filtered = filter_by_category(products, selected_category)
    if filtered:
        display_products_table(filtered, title=f"CATEGORY: {selected_category.upper()}")
    else:
        print(f"\n[Notice] No products found in category '{selected_category}'.")


def smart_optimizer_flow(products):
    """
    Interactive Smart Purchase Optimization Flow.
    Helps users budget, identify expensive items, and optimize cart costs.
    """
    print("\n" + "=" * 65)
    print("         SMART PURCHASE OPTIMIZER & BUDGET PLANNER       ")
    print("=" * 65)

    if not products:
        print(" [Notice] Your shopping list is empty. Add products first.")
        print("=" * 65)
        return

    total_cost = calculate_total_cost(products)
    total_qty = calculate_total_quantity(products)
    most_exp = find_most_expensive_product(products)
    cheapest = find_cheapest_product(products)
    highest_spend = find_highest_spending_product(products)

    print(f"\n[Shopping Cart Summary]")
    print(f"  - Total Products in List : {len(products)}")
    print(f"  - Total Items to Buy     : {total_qty}")
    print(f"  - Total Purchase Cost    : {CURRENCY}{total_cost:.2f}")

    if most_exp:
        print(f"  - Most Expensive Product : {most_exp['name']} ({CURRENCY}{most_exp['price']:.2f} each)")
    if cheapest:
        print(f"  - Cheapest Product       : {cheapest['name']} ({CURRENCY}{cheapest['price']:.2f} each)")
    if highest_spend:
        h_cost = int(highest_spend['quantity']) * float(highest_spend['price'])
        print(f"  - Highest Spending Item  : {highest_spend['name']} ({CURRENCY}{h_cost:.2f} total for {highest_spend['quantity']} units)")

    print("-" * 65)
    budget_input = input(f"Enter your target shopping budget ({CURRENCY}) [or press Enter to skip]: ").strip()

    if not budget_input:
        print("[Notice] Budget analysis skipped.")
        print("=" * 65)
        return

    try:
        budget = float(budget_input)
        if budget <= 0:
            print("[Error] Budget must be greater than 0.")
            return
    except ValueError:
        print("[Error] Invalid budget value. Please enter a valid number.")
        return

    analysis = analyze_budget(products, budget)

    print("\n" + "-" * 65)
    print("                   BUDGET OPTIMIZATION RESULT                   ")
    print("-" * 65)
    print(f" Target Budget        : {CURRENCY}{analysis['budget']:.2f}")
    print(f" Total Cart Cost      : {CURRENCY}{analysis['total_cost']:.2f}")
    print(f" Budget Utilization   : {analysis['percentage_used']:.1f}%")

    if analysis["is_within_budget"]:
        print(f" Status               : [WITHIN BUDGET]")
        print(f" Remaining Savings    : {CURRENCY}{analysis['difference']:.2f}")
        print("\n [Smart Tip] Excellent! Your purchases are safely within your budget.")
    else:
        print(f" Status               : [BUDGET EXCEEDED]")
        print(f" Over Budget By       : {CURRENCY}{analysis['difference']:.2f}")
        print("\n [Smart Recommendations to Save Money]:")

        # 1. Check if any single product exceeds the entire budget
        if analysis["exceeding_items"]:
            print("  ! Critical: The following product(s) exceed your entire budget alone:")
            for item in analysis["exceeding_items"]:
                p = item["product"]
                print(f"    - {p['name']} (Total: {CURRENCY}{item['item_cost']:.2f}, exceeds budget by {CURRENCY}{item['excess']:.2f})")

        # 2. Show largest expenses to reduce
        print("\n  ! Top items consuming your budget (consider reducing quantity or removing):")
        for idx, p in enumerate(analysis["sorted_by_cost"][:3], 1):
            cost = int(p["quantity"]) * float(p["price"])
            pct = (cost / total_cost) * 100 if total_cost > 0 else 0
            print(f"    {idx}. {p['name']} (Qty: {p['quantity']}) - {CURRENCY}{cost:.2f} ({pct:.1f}% of total cart)")

    print("=" * 65)
