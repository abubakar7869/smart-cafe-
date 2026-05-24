"""
PDF Requirement – Task 3 & 2.5 (File Handling – EXAM CRITICAL):
  Save menu to menu.txt, load menu at program start,
  save order receipts to orders.txt.

  PDF example format:
    file << name << "," << price << endl;
  We use CSV-style text files (menu.txt, orders.txt).
"""

import os
from models.exceptions import FileError

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
MENU_FILE = os.path.join(DATA_DIR, "menu.txt")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.txt")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


# ── Menu file handling ────────────────────────────────────────────────────────

def save_menu(menu_items: list) -> None:
    """
    PDF Requirement 2.5: Save menu to menu.txt.
    Format per line: name,price,category,description
    """
    try:
        _ensure_data_dir()
        with open(MENU_FILE, "w", encoding="utf-8") as f:
            for item in menu_items:
                desc = item.description.replace(",", ";")  # escape commas
                f.write(f"{item.name},{item.price},{item.category.value},{desc}\n")
        print(f"[File] Menu saved to {MENU_FILE}")
    except OSError as e:
        raise FileError(f"Failed to save menu: {e}")


def load_menu() -> list[dict]:
    """
    PDF Requirement 2.5: Load menu at program start.
    Returns list of dicts ready for MenuItem.from_dict().
    """
    if not os.path.exists(MENU_FILE):
        return []
    try:
        items = []
        with open(MENU_FILE, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",", 3)
                if len(parts) < 3:
                    print(f"[File] Skipping malformed line {line_no}: {line!r}")
                    continue
                name, price_str, category = parts[0], parts[1], parts[2]
                description = parts[3] if len(parts) == 4 else ""
                try:
                    items.append({
                        "name": name,
                        "price": float(price_str),
                        "category": category,
                        "description": description,
                    })
                except ValueError:
                    print(f"[File] Invalid price on line {line_no}, skipping.")
        print(f"[File] Menu loaded from {MENU_FILE} ({len(items)} items)")
        return items
    except OSError as e:
        raise FileError(f"Failed to load menu: {e}")


# ── Order receipt file handling ───────────────────────────────────────────────

def save_order_receipt(order, customer_name: str = "Guest") -> None:
    """
    PDF Requirement 2.5: Save order receipts to orders.txt.
    Appends each receipt so history is preserved.
    """
    try:
        _ensure_data_dir()
        with open(ORDERS_FILE, "a", encoding="utf-8") as f:
            f.write("=" * 40 + "\n")
            f.write(f"Customer : {customer_name}\n")
            f.write(f"Order #  : {order.order_id}\n")
            f.write(f"Status   : {order.status.value}\n")
            f.write("-" * 40 + "\n")
            for item, qty in zip(order._items, order._quantities):
                f.write(f"  {item.name:<22} x{qty}  Rs.{item.price * qty:.2f}\n")
            f.write("-" * 40 + "\n")
            f.write(f"  Subtotal : Rs.{order.calculate_subtotal():.2f}\n")
            f.write(f"  Tax(5%)  : Rs.{order.calculate_tax():.2f}\n")
            f.write(f"  Total    : Rs.{order.calculate_total():.2f}\n")
            f.write("=" * 40 + "\n\n")
        print(f"[File] Receipt saved to {ORDERS_FILE}")
    except OSError as e:
        raise FileError(f"Failed to save receipt: {e}")
