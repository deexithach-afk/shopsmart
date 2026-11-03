"""
products.py - Product Management Module for ShopSmart

Handles CRUD operations:
- Add Product (with unique ID validation and numeric checks)
- View Products (formatted table view)
- Update Product (modify price, quantity, name, or category)
- Delete Product (with confirmation prompt)
"""

import sys
from storage import save_products

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CURRENCY = "₹"
try:
    CURRENCY.encode(sys.stdout.encoding or "utf-8")
except (UnicodeEncodeError, LookupError):
    CURRENCY = "Rs."


def find_product_by_id(products, product_id):
    """
    Search for a product in the list by its ID.
    
    Args:
        products (list): List of product dictionaries.
        product_id (str): The product ID to find.
        
    Returns:
        dict or None: The product dictionary if found, else None.
    """
    cleaned_id = str(product_id).strip().lower()
    for product in products:
        if str(product.get("id", "")).strip().lower() == cleaned_id:
            return product
    return None


def display_products_table(products, title="CURRENT PRODUCTS"):
    """
    Display products in a formatted, clean table.
    
    Args:
        products (list): List of product dictionaries to display.
        title (str): Title header for the table.
    """
    if not products:
        print("\n" + "=" * 70)
        print(f" {title} ")
        print("=" * 70)
        print(" No products found.")
        print("=" * 70)
        return

    print("\n" + "=" * 72)
    print(f" {title.center(70)} ")
    print("=" * 72)
    print(f"{'ID':<8} {'Product':<20} {'Category':<15} {'Qty':<6} {'Price':<11} {'Total':<11}")
    print("-" * 72)

    grand_total = 0.0
    total_qty = 0

    for p in products:
        p_id = str(p.get("id", "N/A"))
        name = str(p.get("name", "N/A"))
        category = str(p.get("category", "General"))
        qty = int(p.get("quantity", 0))
        price = float(p.get("price", 0.0))
        item_total = qty * price

        grand_total += item_total
        total_qty += qty

        # Truncate long strings gracefully for alignment
        if len(name) > 18:
            name = name[:15] + "..."
        if len(category) > 13:
            category = category[:10] + "..."

        price_str = f"{CURRENCY}{price:.2f}"
        total_str = f"{CURRENCY}{item_total:.2f}"
        print(f"{p_id:<8} {name:<20} {category:<15} {qty:<6} {price_str:<11} {total_str:<11}")

    print("-" * 72)
    grand_total_str = f"{CURRENCY}{grand_total:.2f}"
    print(f"Total Unique Items: {len(products):<4} | Total Units: {total_qty:<4} | Cart Total: {grand_total_str}")
    print("=" * 72)


def add_product(products):
    """
    Prompt user for product details, validate inputs, add to list, and save to storage.
    """
    print("\n----- ADD NEW PRODUCT -----")

    # 1. Product ID (must be non-empty and unique)
    while True:
        product_id = input("Enter Product ID: ").strip()
        if not product_id:
            print("[Error] Product ID cannot be empty. Please enter a valid ID.")
            continue
        if find_product_by_id(products, product_id) is not None:
            print(f"[Error] Product with ID '{product_id}' already exists! Please use a unique ID.")
            continue
        break

    # 2. Product Name
    while True:
        name = input("Enter Product Name: ").strip()
        if not name:
            print("[Error] Product Name cannot be empty. Please try again.")
            continue
        break

    # 3. Category
    while True:
        category = input("Enter Category (e.g. Grocery, Clothing, Electronics): ").strip()
        if not category:
            print("[Error] Category cannot be empty. Please try again.")
            continue
        category = category.title()
        break

    # 4. Quantity (must be positive integer)
    while True:
        qty_input = input("Enter Quantity: ").strip()
        try:
            quantity = int(qty_input)
            if quantity <= 0:
                print("[Error] Quantity must be greater than 0.")
                continue
            break
        except ValueError:
            print("[Error] Invalid input! Quantity must be a whole number (integer).")

    # 5. Price (must be positive float)
    while True:
        price_input = input(f"Enter Price ({CURRENCY}): ").strip()
        try:
            price = float(price_input)
            if price <= 0:
                print("[Error] Price must be greater than 0.")
                continue
            break
        except ValueError:
            print("[Error] Invalid input! Price must be a valid number.")

    # Create new product dictionary
    new_product = {
        "id": product_id,
        "name": name,
        "category": category,
        "quantity": quantity,
        "price": round(price, 2)
    }

    products.append(new_product)
    if save_products(products):
        print(f"\n[Success] Product '{name}' (ID: {product_id}) added successfully!")
        return True
    else:
        print("\n[Warning] Product was added to session, but failed to save to storage file.")
        return False


def view_products(products):
    """
    Display all stored products in a table format.
    """
    display_products_table(products, title="ALL REGISTERED PRODUCTS")


def update_product(products):
    """
    Update an existing product's price, quantity, name, or category.
    """
    print("\n----- UPDATE PRODUCT -----")
    if not products:
        print("[Notice] Inventory is empty. No products available to update.")
        return False

    product_id = input("Enter Product ID to update: ").strip()
    product = find_product_by_id(products, product_id)

    if product is None:
        print(f"[Error] Product with ID '{product_id}' not found.")
        return False

    print("\nCurrent Product Details:")
    print(f"ID       : {product.get('id')}")
    print(f"Name     : {product.get('name')}")
    print(f"Category : {product.get('category')}")
    print(f"Quantity : {product.get('quantity')}")
    print(f"Price    : {CURRENCY}{product.get('price'):.2f}")

    print("\nWhat would you like to update?")
    print("1. Price")
    print("2. Quantity")
    print("3. Product Name")
    print("4. Category")
    print("5. Update Price & Quantity")
    print("6. Cancel")

    choice = input("Enter choice (1-6): ").strip()

    if choice == "1":
        while True:
            try:
                new_price = float(input(f"Enter new price (Current: {CURRENCY}{product['price']:.2f}): {CURRENCY}").strip())
                if new_price <= 0:
                    print("[Error] Price must be greater than 0.")
                    continue
                product["price"] = round(new_price, 2)
                break
            except ValueError:
                print("[Error] Invalid price format. Please enter a number.")

    elif choice == "2":
        while True:
            try:
                new_qty = int(input(f"Enter new quantity (Current: {product['quantity']}): ").strip())
                if new_qty <= 0:
                    print("[Error] Quantity must be greater than 0.")
                    continue
                product["quantity"] = new_qty
                break
            except ValueError:
                print("[Error] Invalid quantity format. Please enter a whole number.")

    elif choice == "3":
        new_name = input(f"Enter new name (Current: {product['name']}): ").strip()
        if new_name:
            product["name"] = new_name
        else:
            print("[Notice] Name unchanged.")

    elif choice == "4":
        new_cat = input(f"Enter new category (Current: {product['category']}): ").strip()
        if new_cat:
            product["category"] = new_cat.title()
        else:
            print("[Notice] Category unchanged.")

    elif choice == "5":
        # Update both price & quantity
        while True:
            try:
                new_price = float(input(f"Enter new price (Current: {CURRENCY}{product['price']:.2f}): {CURRENCY}").strip())
                if new_price <= 0:
                    print("[Error] Price must be greater than 0.")
                    continue
                product["price"] = round(new_price, 2)
                break
            except ValueError:
                print("[Error] Invalid price. Please enter a valid number.")

        while True:
            try:
                new_qty = int(input(f"Enter new quantity (Current: {product['quantity']}): ").strip())
                if new_qty <= 0:
                    print("[Error] Quantity must be greater than 0.")
                    continue
                product["quantity"] = new_qty
                break
            except ValueError:
                print("[Error] Invalid quantity. Please enter a whole number.")

    elif choice == "6":
        print("[Notice] Update cancelled.")
        return False
    else:
        print("[Error] Invalid choice selected. Update cancelled.")
        return False

    if save_products(products):
        print(f"\n[Success] Product '{product['name']}' (ID: {product['id']}) updated successfully!")
        return True
    return False


def delete_product(products):
    """
    Delete a product using its ID after user confirmation.
    """
    print("\n----- DELETE PRODUCT -----")
    if not products:
        print("[Notice] Inventory is empty. No products to delete.")
        return False

    product_id = input("Enter Product ID to delete: ").strip()
    product = find_product_by_id(products, product_id)

    if product is None:
        print(f"[Error] Product with ID '{product_id}' not found.")
        return False

    # Confirm before deleting
    confirm = input(
        f"Are you sure you want to delete '{product['name']}' (ID: {product['id']})? (y/n): "
    ).strip().lower()

    if confirm in ["y", "yes"]:
        products.remove(product)
        if save_products(products):
            print(f"\n[Success] Product '{product['name']}' (ID: {product_id}) deleted successfully!")
            return True
        else:
            print("\n[Warning] Product removed from session, but failed to update file storage.")
            return False
    else:
        print("[Notice] Product deletion cancelled.")
        return False
