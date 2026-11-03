"""
test_shopsmart.py - Automated Verification Test Suite for ShopSmart
Tests all core functions and modules non-interactively.
"""

import os
import json
import storage
import products
import operations
import reports


def test_storage():
    test_file = "test_products.json"
    sample = [
        {"id": "1", "name": "Pen", "category": "Stationery", "quantity": 10, "price": 15.0}
    ]
    # Test saving
    assert storage.save_products(sample, filename=test_file) is True
    # Test loading
    loaded = storage.load_products(filename=test_file)
    assert len(loaded) == 1
    assert loaded[0]["name"] == "Pen"
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)
    print("[PASS] storage.py tests passed.")


def test_products_lookup():
    sample = [
        {"id": "101", "name": "Rice", "category": "Grocery", "quantity": 2, "price": 60.0},
        {"id": "102", "name": "Shirt", "category": "Clothing", "quantity": 1, "price": 500.0}
    ]
    p1 = products.find_product_by_id(sample, "101")
    assert p1 is not None and p1["name"] == "Rice"
    
    p2 = products.find_product_by_id(sample, "999")
    assert p2 is None
    print("[PASS] products.py lookup tests passed.")


def test_operations():
    sample = [
        {"id": "101", "name": "Rice", "category": "Grocery", "quantity": 2, "price": 60.0},     # 120
        {"id": "102", "name": "Shirt", "category": "Clothing", "quantity": 1, "price": 500.0},  # 500
        {"id": "103", "name": "Milk", "category": "Grocery", "quantity": 3, "price": 30.0},      # 90
        {"id": "104", "name": "Headphones", "category": "Electronics", "quantity": 1, "price": 1200.0} # 1200
    ]
    
    # Search by name
    res = operations.search_by_name(sample, "ric")
    assert len(res) == 1 and res[0]["name"] == "Rice"
    
    # Filter by category
    groceries = operations.filter_by_category(sample, "grocery")
    assert len(groceries) == 2
    
    # Filter by price range
    mid_range = operations.filter_by_price_range(sample, 50, 600)
    assert len(mid_range) == 2  # Rice (60) and Shirt (500)
    
    # Calculations
    total_cost = operations.calculate_total_cost(sample)
    # 2*60 + 1*500 + 3*30 + 1*1200 = 120 + 500 + 90 + 1200 = 1910.0
    assert total_cost == 1910.0
    
    total_qty = operations.calculate_total_quantity(sample)
    # 2 + 1 + 3 + 1 = 7
    assert total_qty == 7
    
    most_exp = operations.find_most_expensive_product(sample)
    assert most_exp["name"] == "Headphones"
    
    cheapest = operations.find_cheapest_product(sample)
    assert cheapest["name"] == "Milk"
    
    # Budget analysis - within budget
    b_analysis1 = operations.analyze_budget(sample, 2000.0)
    assert b_analysis1["is_within_budget"] is True
    assert b_analysis1["difference"] == 90.0
    
    # Budget analysis - exceeded
    b_analysis2 = operations.analyze_budget(sample, 1000.0)
    assert b_analysis2["is_within_budget"] is False
    assert b_analysis2["difference"] == 910.0
    # Headphones cost 1200, which exceeds 1000 alone
    assert len(b_analysis2["exceeding_items"]) == 1
    assert b_analysis2["exceeding_items"][0]["product"]["name"] == "Headphones"
    
    # Category spending
    cat_spend = operations.calculate_category_spending(sample)
    assert "Grocery" in cat_spend
    assert cat_spend["Grocery"]["total_cost"] == 210.0
    assert cat_spend["Clothing"]["total_cost"] == 500.0
    assert cat_spend["Electronics"]["total_cost"] == 1200.0
    
    print("[PASS] operations.py tests passed.")


def test_reports_export():
    sample = [
        {"id": "101", "name": "Rice", "category": "Grocery", "quantity": 2, "price": 60.0}
    ]
    cat_summary = operations.calculate_category_spending(sample)
    reports.export_report_to_file(
        total_products=1,
        total_units=2,
        total_cost=120.0,
        most_exp=sample[0],
        cheapest=sample[0],
        category_summary=cat_summary,
        budget_status="WITHIN BUDGET"
    )
    assert os.path.exists("shopping_report.txt")
    with open("shopping_report.txt", "r", encoding="utf-8") as f:
        content = f.read()
    assert "SHOPSMART - SHOPPING REPORT" in content
    assert "Rice" in content
    
    # Cleanup
    if os.path.exists("shopping_report.txt"):
        os.remove("shopping_report.txt")
    print("[PASS] reports.py export test passed.")


if __name__ == "__main__":
    print("Running ShopSmart automated tests...")
    test_storage()
    test_products_lookup()
    test_operations()
    test_reports_export()
    print("\nALL AUTOMATED TESTS PASSED SUCCESSFULLY!")

