9"""
main.py - Main Entry Point for ShopSmart - Smart Purchase Optimizer

Project: ShopSmart – Smart Purchase Optimizer
Objective: Help users manage products, track purchases, organize categories,
           and optimize budget using Python fundamentals.

Modules:
1. User Menu (main loop)
2. Add Product
3. View Products
4. Update & Delete Product
5. Search & Filter (by name, category, price range)
6. Smart Purchase Optimization (cost, budget check, extreme prices)
7. Generate Reports
8. File Storage (JSON persistence)
"""

import sys

# Ensure UTF-8 output encoding across Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from storage import initialize_default_file, save_products
from products import (
    add_product,
    view_products,
    update_product,
    delete_product
)
from operations import (
    search_product_flow,
    filter_category_flow,
    smart_optimizer_flow
)
from reports import generate_report


def display_menu():
    """
    Display the main user menu as specified in Module 1.
    """
    print("\n===== SHOPSMART =====")
    print("1. Add Product")
    print("2. View Products")
    print("3. Update Product")
    print("4. Delete Product")
    print("5. Search Product")
    print("6. Filter by Category")
    print("7. Generate Report")
    print("8. Exit")


def main():
    """
    Main application loop.
    """
    print("=" * 50)
    print("   WELCOME TO SHOPSMART - SMART PURCHASE OPTIMIZER   ")
    print("=" * 50)

    # Load or initialize products from JSON storage
    products = initialize_default_file()
    print(f"[System] Loaded {len(products)} product(s) from 'products.json'.")

    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_product(products)

        elif choice == "2":
            view_products(products)

        elif choice == "3":
            update_product(products)

        elif choice == "4":
            delete_product(products)

        elif choice == "5":
            search_product_flow(products)

        elif choice == "6":
            filter_category_flow(products)

        elif choice == "7":
            generate_report(products)

        elif choice == "8":
            # Save final state before exiting
            save_products(products)
            print("\nThank you for using ShopSmart! Your data is saved. Goodbye!")
            sys.exit(0)

        elif choice.lower() in ["9", "smart", "optimizer", "opt"]:
            # Bonus direct shortcut to Smart Purchase Optimizer
            smart_optimizer_flow(products)

        else:
            print("\n[Error] Invalid choice! Please enter a number between 1 and 8.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[System] Program interrupted by user. Exiting safely...")
        sys.exit(0)
