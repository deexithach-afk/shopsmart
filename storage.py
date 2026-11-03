"""
storage.py - Data Persistence Module for ShopSmart

Handles saving and loading product data to/from a JSON file.
Demonstrates:
- File handling (open with context manager)
- JSON serialization and deserialization
- Exception handling (FileNotFoundError, JSONDecodeError, IOError)
"""

import json
import os

DEFAULT_DATA_FILE = "products.json"


def load_products(filename=DEFAULT_DATA_FILE):
    """
    Load products from a JSON file.
    
    Returns:
        list: A list of product dictionaries. Returns an empty list if file
              does not exist or contains invalid JSON data.
    """
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                print(f"[Warning] Invalid format in '{filename}'. Expected a list.")
                return []
    except json.JSONDecodeError:
        print(f"[Warning] '{filename}' is corrupted or empty. Initializing empty product list.")
        return []
    except IOError as e:
        print(f"[Error] Failed to read '{filename}': {e}")
        return []


def save_products(products, filename=DEFAULT_DATA_FILE):
    """
    Save the list of products to a JSON file.
    
    Args:
        products (list): The list of product dictionaries to save.
        filename (str): The destination JSON file path.
        
    Returns:
        bool: True if save succeeded, False otherwise.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(products, file, indent=4)
        return True
    except IOError as e:
        print(f"[Error] Failed to save products to '{filename}': {e}")
        return False


def initialize_default_file(filename=DEFAULT_DATA_FILE, sample_products=None):
    """
    Creates the JSON file with sample data if it doesn't already exist.
    """
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        if sample_products is None:
            sample_products = [
                {"id": "101", "name": "Rice", "category": "Grocery", "quantity": 2, "price": 60.0},
                {"id": "102", "name": "Shirt", "category": "Clothing", "quantity": 1, "price": 500.0},
                {"id": "103", "name": "Milk", "category": "Grocery", "quantity": 3, "price": 30.0},
                {"id": "104", "name": "Headphones", "category": "Electronics", "quantity": 1, "price": 1200.0},
                {"id": "105", "name": "Apple", "category": "Grocery", "quantity": 6, "price": 25.0}
            ]
        save_products(sample_products, filename)
        return sample_products
    return load_products(filename)
