"""
auth.py - User Authentication and Management Module for ShopSmart

Handles:
- Loading and saving user accounts in users.json
- Password hashing with hashlib.sha256
- User login authentication
- New user registration
"""

import hashlib
import json
import os

USERS_FILE = "users.json"


def load_users():
    """Load users list from JSON file. If not present, initialize default users."""
    if not os.path.exists(USERS_FILE):
        return initialize_default_users()

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
            if isinstance(users, list):
                return users
            return initialize_default_users()
    except (json.JSONDecodeError, IOError):
        return initialize_default_users()


def save_users(users):
    """Save users list to JSON file."""
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)
        return True
    except IOError as e:
        print(f"[Error] Failed to save users: {e}")
        return False


def initialize_default_users():
    """Create initial default admin and demo user accounts."""
    default_users = [
        {
            "username": "admin",
            "password_hash": "7b54062d0c4a72e186ebed296a1d390374a8b137f5a3a5cbf522173a787b10d8",
            "name": "Administrator",
            "role": "Admin"
        },
        {
            "username": "shopper",
            "password_hash": "24d5343ee97a5811acdf8ca9669134b8412b9d98a04f2f8b60e8d887afa8c484",
            "name": "Demo Shopper",
            "role": "User"
        }
    ]
    save_users(default_users)
    return default_users


def authenticate_user(username, password):
    """Authenticate a user by username and password."""
    clean_user = username.strip().lower()
    users = load_users()
    
    hashed_input = hashlib.sha256(("shopsmart_salt_2026" + password).encode("utf-8")).hexdigest()

    for u in users:
        if u.get("username", "").lower() == clean_user:
            if u.get("password_hash") == hashed_input:
                return {
                    "username": u.get("username"),
                    "name": u.get("name", u.get("username")),
                    "role": u.get("role", "User")
                }, "Login successful"
            else:
                return None, "Invalid password. Please try again."

    return None, f"No user account found with username '{username}'."


def register_user(username, password, name=""):
    """Register a new user account."""
    clean_user = username.strip().lower()
    if not clean_user or len(clean_user) < 3:
        return None, "Username must be at least 3 characters long."

    if not password or len(password) < 4:
        return None, "Password must be at least 4 characters long."

    users = load_users()
    for u in users:
        if u.get("username", "").lower() == clean_user:
            return None, f"Username '{username}' is already taken. Please choose another."

    display_name = name.strip() if name and name.strip() else username.strip().capitalize()
    new_user = {
        "username": clean_user,
        "password_hash": hashlib.sha256(("shopsmart_salt_2026" + password).encode("utf-8")).hexdigest(),
        "name": display_name,
        "role": "User"
    }

    users.append(new_user)
    if save_users(users):
        return {
            "username": new_user["username"],
            "name": new_user["name"],
            "role": new_user["role"]
        }, "Registration successful!"
    else:
        return None, "Failed to save user data."
