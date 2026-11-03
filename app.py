"""
app.py - Web Server & Localhost Interface for ShopSmart

Runs a zero-dependency HTTP server on http://localhost:5000
Features:
- Landing Page (Index Page) at /
- Login & Register Page at /login
- Smart Dashboard at /dashboard
- Product CRUD & Category API
- Smart Purchase Optimizer
- User Authentication (auth.py & users.json)
- Downloadable Reports
"""

import http.server
import json
import os
import sys
import urllib.parse

from storage import load_products, save_products, DEFAULT_DATA_FILE
from operations import (
    calculate_total_cost,
    calculate_total_quantity,
    find_most_expensive_product,
    find_cheapest_product,
    calculate_category_spending,
    analyze_budget,
    get_unique_categories
)
import auth

PORT = 5000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")


def read_template(filename):
    """Read HTML template from templates folder with fallback."""
    filepath = os.path.join(TEMPLATES_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return f"<h1>Template '{filename}' not found.</h1>"


class ShopSmartWebHandler(http.server.BaseHTTPRequestHandler):
    def _send_response_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def _send_response_html(self, html_content, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 1. Page Routes
        if path == "/" or path == "/index.html":
            html = read_template("index.html")
            self._send_response_html(html)

        elif path == "/login" or path == "/login.html":
            html = read_template("login.html")
            self._send_response_html(html)

        elif path == "/dashboard" or path == "/dashboard.html":
            html = read_template("dashboard.html")
            self._send_response_html(html)

        # 2. API Routes
        elif path == "/api/products":
            products = load_products()
            self._send_response_json(products)

        elif path == "/api/categories":
            products = load_products()
            cats = get_unique_categories(products)
            self._send_response_json(cats)

        elif path == "/api/report/export":
            # Text file download of the report
            products = load_products()
            total_products = len(products)
            total_units = calculate_total_quantity(products)
            total_cost = calculate_total_cost(products)
            most_exp = find_most_expensive_product(products)
            cheapest = find_cheapest_product(products)
            category_summary = calculate_category_spending(products)

            most_exp_str = f"{most_exp['name']} (₹{most_exp['price']:.2f})" if most_exp else "None"
            cheapest_str = f"{cheapest['name']} (₹{cheapest['price']:.2f})" if cheapest else "None"

            lines = [
                "======================================================================",
                "                   SHOPSMART - SHOPPING REPORT                        ",
                "======================================================================\n",
                f"Total Unique Products  : {total_products}",
                f"Total Item Units       : {total_units}",
                f"Total Shopping Cost    : ₹{total_cost:,.2f}",
                f"Most Expensive Product : {most_exp_str}",
                f"Cheapest Product       : {cheapest_str}\n",
                "CATEGORY-WISE EXPENDITURE:",
                f"{'Category':<20} {'Items':<8} {'Units':<8} {'Total':<15} {'% Share'}",
                "-" * 65
            ]
            for cat, data in category_summary.items():
                lines.append(f"{cat:<20} {data['count']:<8} {data['quantity']:<8} ₹{data['total_cost']:<14.2f} {data['percentage']}%")
            lines.append("-" * 65 + "\n")

            content = "\n".join(lines)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Disposition", "attachment; filename=shopping_report.txt")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")

        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._send_response_json({"error": "Invalid JSON payload."}, 400)
            return

        # Login endpoint
        if parsed.path == "/api/login":
            username = str(data.get("username", "")).strip()
            password = str(data.get("password", "")).strip()

            user, msg = auth.authenticate_user(username, password)
            if user:
                self._send_response_json({"message": msg, "user": user})
            else:
                self._send_response_json({"error": msg}, 401)

        # Register endpoint
        elif parsed.path == "/api/register":
            name = str(data.get("name", "")).strip()
            username = str(data.get("username", "")).strip()
            password = str(data.get("password", "")).strip()

            user, msg = auth.register_user(username, password, name)
            if user:
                self._send_response_json({"message": msg, "user": user}, 201)
            else:
                self._send_response_json({"error": msg}, 400)

        # Products Add endpoint
        elif parsed.path == "/api/products":
            try:
                products = load_products()
                p_id = str(data.get("id", "")).strip()
                name = str(data.get("name", "")).strip()
                cat = str(data.get("category", "")).strip().title()
                qty = int(data.get("quantity", 0))
                price = float(data.get("price", 0.0))

                if not p_id or not name or not cat or qty <= 0 or price <= 0:
                    self._send_response_json({"error": "Invalid fields. All fields required and must be positive."}, 400)
                    return

                for p in products:
                    if str(p.get("id", "")).strip().lower() == p_id.lower():
                        self._send_response_json({"error": f"Product with ID '{p_id}' already exists!"}, 400)
                        return

                new_product = {
                    "id": p_id,
                    "name": name,
                    "category": cat,
                    "quantity": qty,
                    "price": round(price, 2)
                }
                products.append(new_product)
                save_products(products)
                self._send_response_json({"message": "Product added successfully", "product": new_product}, 201)

            except (ValueError, TypeError) as e:
                self._send_response_json({"error": f"Bad request: {str(e)}"}, 400)

        else:
            self.send_response(404)
            self.end_headers()

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/products":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            try:
                data = json.loads(body)
                products = load_products()
                p_id = str(data.get("id", "")).strip().lower()

                target = None
                for p in products:
                    if str(p.get("id", "")).strip().lower() == p_id:
                        target = p
                        break

                if not target:
                    self._send_response_json({"error": "Product not found."}, 404)
                    return

                if "name" in data and str(data["name"]).strip():
                    target["name"] = str(data["name"]).strip()
                if "category" in data and str(data["category"]).strip():
                    target["category"] = str(data["category"]).strip().title()
                if "quantity" in data and int(data["quantity"]) > 0:
                    target["quantity"] = int(data["quantity"])
                if "price" in data and float(data["price"]) > 0:
                    target["price"] = round(float(data["price"]), 2)

                save_products(products)
                self._send_response_json({"message": "Product updated successfully", "product": target})

            except (ValueError, json.JSONDecodeError) as e:
                self._send_response_json({"error": f"Bad request: {str(e)}"}, 400)
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/products":
            query = urllib.parse.parse_qs(parsed.query)
            p_id = query.get("id", [""])[0].strip().lower()

            products = load_products()
            initial_len = len(products)
            products = [p for p in products if str(p.get("id", "")).strip().lower() != p_id]

            if len(products) < initial_len:
                save_products(products)
                self._send_response_json({"message": "Product deleted successfully."})
            else:
                self._send_response_json({"error": "Product not found."}, 404)
        else:
            self.send_response(404)
            self.end_headers()


def run_server(port=PORT):
    server_address = ("127.0.0.1", port)
    httpd = http.server.HTTPServer(server_address, ShopSmartWebHandler)
    print("=" * 60)
    print(f"🚀 ShopSmart Web Application is LIVE on Localhost!")
    print(f"👉 Home (Index):     http://localhost:{port}/")
    print(f"👉 Login:            http://localhost:{port}/login")
    print(f"👉 Dashboard:        http://localhost:{port}/dashboard")
    print("=" * 60)
    print("Press Ctrl + C in terminal to stop server.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[System] Stopping ShopSmart server gracefully...")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
