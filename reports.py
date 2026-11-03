"""
reports.py - Shopping Reports and Analytics Module for ShopSmart

Generates comprehensive reports covering:
- Total number of unique products & total item units
- Total shopping expenditure
- Most expensive and cheapest products
- Category-wise spending breakdown (count, amount, and percentage)
- Budget status (compares against user budget)
- Optional report export to file
"""

import sys
from products import CURRENCY
from operations import (
    calculate_total_cost,
    calculate_total_quantity,
    find_most_expensive_product,
    find_cheapest_product,
    calculate_category_spending,
    analyze_budget
)

# Ensure UTF-8 output encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def generate_report(products):
    """
    Generate and print a detailed shopping report displaying all Module 7 requirements.
    
    Requirements displayed:
    1. Total number of products
    2. Total shopping cost
    3. Category-wise spending
    4. Most expensive product (and cheapest)
    5. Budget status
    """
    print("\n" + "=" * 70)
    print("                 SHOPSMART - COMPREHENSIVE REPORT               ")
    print("=" * 70)

    if not products:
        print(" [Notice] No products available in the system to generate a report.")
        print("=" * 70)
        return

    # Basic Metrics
    total_products = len(products)
    total_units = calculate_total_quantity(products)
    total_cost = calculate_total_cost(products)
    most_exp = find_most_expensive_product(products)
    cheapest = find_cheapest_product(products)
    category_summary = calculate_category_spending(products)

    # 1. Summary Metrics
    print("\n[1. OVERVIEW & EXPENDITURE SUMMARY]")
    print(f"  * Total Unique Products   : {total_products}")
    print(f"  * Total Quantity (Units)  : {total_units}")
    print(f"  * Total Shopping Cost     : {CURRENCY}{total_cost:,.2f}")
    if total_units > 0:
        avg_item_cost = total_cost / total_units
        print(f"  * Average Cost per Unit   : {CURRENCY}{avg_item_cost:.2f}")

    # 2. Extremes
    print("\n[2. PRICE EXTREMES]")
    if most_exp:
        print(f"  * Most Expensive Product  : {most_exp['name']} ({most_exp['category']}) - {CURRENCY}{most_exp['price']:.2f}")
    if cheapest:
        print(f"  * Cheapest Product        : {cheapest['name']} ({cheapest['category']}) - {CURRENCY}{cheapest['price']:.2f}")

    # 3. Category-Wise Spending
    print("\n[3. CATEGORY-WISE SPENDING BREAKDOWN]")
    print(f"  {'Category':<18} {'Items':<8} {'Units':<8} {'Total Spent':<15} {'% Share':<8}")
    print("  " + "-" * 60)
    for cat, data in category_summary.items():
        total_spent_str = f"{CURRENCY}{data['total_cost']:<13.2f}"
        print(f"  {cat:<18} {data['count']:<8} {data['quantity']:<8} {total_spent_str} {data['percentage']}%")
    print("  " + "-" * 60)

    # 4. Budget Status
    print("\n[4. SMART BUDGET STATUS]")
    budget_input = input(f"  Enter your shopping budget ({CURRENCY}) [Press Enter to skip]: ").strip()
    budget_report_text = ""

    if budget_input:
        try:
            budget = float(budget_input)
            analysis = analyze_budget(products, budget)
            print(f"  * Shopping Budget   : {CURRENCY}{analysis['budget']:,.2f}")
            print(f"  * Total Spent       : {CURRENCY}{analysis['total_cost']:,.2f}")
            print(f"  * Utilization       : {analysis['percentage_used']:.1f}%")

            if analysis["is_within_budget"]:
                print(f"  * Budget Status     : [WITHIN BUDGET] - Savings: {CURRENCY}{analysis['difference']:,.2f}")
                budget_report_text = f"Budget: {CURRENCY}{analysis['budget']:.2f} | Spent: {CURRENCY}{analysis['total_cost']:.2f} | Status: WITHIN BUDGET (Savings: {CURRENCY}{analysis['difference']:.2f})"
            else:
                print(f"  * Budget Status     : [BUDGET EXCEEDED] - Deficit: {CURRENCY}{analysis['difference']:,.2f}")
                budget_report_text = f"Budget: {CURRENCY}{analysis['budget']:.2f} | Spent: {CURRENCY}{analysis['total_cost']:.2f} | Status: BUDGET EXCEEDED (Over by: {CURRENCY}{analysis['difference']:.2f})"

                if analysis["exceeding_items"]:
                    print("\n  * Products Exceeding Entire Budget:")
                    for item in analysis["exceeding_items"]:
                        p = item["product"]
                        print(f"    - {p['name']} (Cost: {CURRENCY}{item['item_cost']:.2f})")
        except ValueError:
            print("  [Warning] Invalid budget input. Budget analysis omitted.")
            budget_report_text = "Budget status: Not evaluated."
    else:
        print("  * Budget Status     : No budget specified.")
        budget_report_text = "Budget status: No budget specified."

    print("\n" + "=" * 70)

    # Optional: Export Report to a file
    export_choice = input("Would you like to export this report to a text file? (y/n) [Default n]: ").strip().lower()
    if export_choice in ["y", "yes"]:
        export_report_to_file(
            total_products, total_units, total_cost, most_exp, cheapest, category_summary, budget_report_text
        )


def export_report_to_file(total_products, total_units, total_cost, most_exp, cheapest, category_summary, budget_status):
    """
    Saves the generated report to 'shopping_report.txt'.
    """
    filename = "shopping_report.txt"
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("======================================================================\n")
            file.write("                   SHOPSMART - SHOPPING REPORT                        \n")
            file.write("======================================================================\n\n")
            file.write(f"Total Unique Products  : {total_products}\n")
            file.write(f"Total Item Units       : {total_units}\n")
            file.write(f"Total Shopping Cost    : {CURRENCY}{total_cost:,.2f}\n")
            if most_exp:
                file.write(f"Most Expensive Product : {most_exp['name']} ({CURRENCY}{most_exp['price']:.2f})\n")
            if cheapest:
                file.write(f"Cheapest Product       : {cheapest['name']} ({CURRENCY}{cheapest['price']:.2f})\n\n")

            file.write("CATEGORY-WISE EXPENDITURE:\n")
            file.write(f"{'Category':<20} {'Items':<8} {'Units':<8} {'Total':<15} {'% Share'}\n")
            file.write("-" * 65 + "\n")
            for cat, data in category_summary.items():
                total_str = f"{CURRENCY}{data['total_cost']:<13.2f}"
                file.write(f"{cat:<20} {data['count']:<8} {data['quantity']:<8} {total_str} {data['percentage']}%\n")
            file.write("-" * 65 + "\n\n")

            file.write(f"BUDGET STATUS:\n{budget_status}\n\n")
            file.write("======================================================================\n")

        print(f"[Success] Report exported successfully to '{filename}'!")
    except IOError as e:
        print(f"[Error] Failed to export report to file: {e}")
