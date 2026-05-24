"""
PDF Requirement – Task 1 & Task 2:
  Order class: multiple items, quantity, remove item,
  subtotal, tax (5%), total + formatted receipt.
"""

from models.menu_item import MenuItem
from models.enums import Category, OrderStatus

TAX_RATE = 0.05  # 5% as specified in PDF


class Order:
    """
    Represents a single customer order.

    PDF Requirement:
      vector<MenuItem> items  →  self._items (list of MenuItem)
      vector<int> quantity    →  self._quantities (list of int)
      addItem(), removeItem(), calculateTotal()
    """

    _id_counter = 1  # auto-increment order IDs

    def __init__(self):
        self._order_id = Order._id_counter
        Order._id_counter += 1
        self._items: list[MenuItem] = []
        self._quantities: list[int] = []
        self._status = OrderStatus.Pending

    # ── Properties ────────────────────────────────────────────────────────────
    @property
    def order_id(self) -> int:
        return self._order_id

    @property
    def status(self) -> OrderStatus:
        return self._status

    @status.setter
    def status(self, value: OrderStatus):
        self._status = value

    # ── Add item ──────────────────────────────────────────────────────────────
    def add_item(self, item: MenuItem, qty: int = 1):
        """PDF Requirement: addItem(MenuItem item, int qty)."""
        if qty <= 0:
            raise ValueError("Quantity must be at least 1.")
        # if item already in order, increase quantity
        for i, existing in enumerate(self._items):
            if existing.name.lower() == item.name.lower() and existing.category == item.category:
                self._quantities[i] += qty
                return
        self._items.append(item)
        self._quantities.append(qty)

    # ── Remove item ───────────────────────────────────────────────────────────
    def remove_item(self, item_name: str, category: Category = None):
        """PDF Requirement: removeItem(string itemName) — important for POS."""
        for i, item in enumerate(self._items):
            name_match = item.name.lower() == item_name.lower()
            cat_match = (category is None) or (item.category == category)
            if name_match and cat_match:
                self._items.pop(i)
                self._quantities.pop(i)
                print(f"[Order #{self._order_id}] '{item_name}' removed.")
                return
        raise ValueError(f"'{item_name}' not found in order.")

    # ── Change quantity ───────────────────────────────────────────────────────
    def change_quantity(self, item_name: str, category: Category, new_qty: int):
        """PDF Requirement: update quantity of an existing item."""
        if new_qty <= 0:
            raise ValueError("New quantity must be at least 1.")
        for i, item in enumerate(self._items):
            if item.name.lower() == item_name.lower() and item.category == category:
                self._quantities[i] = new_qty
                return
        raise ValueError(f"'{item_name}' not found in order.")

    # ── Calculate total (PDF Task 2) ──────────────────────────────────────────
    def calculate_subtotal(self) -> float:
        return sum(
            item.price * qty for item, qty in zip(self._items, self._quantities)
        )

    def calculate_tax(self) -> float:
        return round(self.calculate_subtotal() * TAX_RATE, 2)

    def calculate_total(self) -> float:
        """PDF Requirement: calculateTotal() including 5% tax."""
        return round(self.calculate_subtotal() + self.calculate_tax(), 2)

    def is_empty(self) -> bool:
        return len(self._items) == 0

    # ── Formatted receipt (PDF 2.6 Billing System) ────────────────────────────
    def print_receipt(self, customer_name: str = "Guest", discount: float = 0.0):
        """
        PDF Requirement 2.6 – formatted receipt.
        Optional discount for bonus feature (10% student discount).
        """
        if self.is_empty():
            raise RuntimeError("Order is empty! Cannot print receipt.")  # PDF 2.7

        subtotal = self.calculate_subtotal()
        tax = round(subtotal * TAX_RATE, 2)
        discount_amt = round(subtotal * discount, 2)
        total = round(subtotal + tax - discount_amt, 2)

        print("\n" + "─" * 40)
        print("        Smart Cafe – Receipt")
        print("─" * 40)
        print(f"  Customer : {customer_name}")
        print(f"  Order #  : {self._order_id}")
        print("─" * 40)
        print(f"  {'Item':<22} {'Qty':>4} {'Price':>8}")
        print("─" * 40)
        for item, qty in zip(self._items, self._quantities):
            line_total = item.price * qty
            print(f"  {item.name:<22} {qty:>4} {line_total:>8.2f}")
        print("─" * 40)
        print(f"  {'Subtotal':<30} {subtotal:>7.2f}")
        print(f"  {'Tax (5%)':<30} {tax:>7.2f}")
        if discount_amt > 0:
            print(f"  {'Discount':<30} -{discount_amt:>6.2f}")
        print(f"  {'TOTAL':<30} {total:>7.2f}")
        print("─" * 40)
        print(f"  Status: {self._status.value}")
        print("─" * 40 + "\n")

    # ── str ───────────────────────────────────────────────────────────────────
    def __str__(self):
        if self.is_empty():
            return f"Order #{self._order_id} [Empty] | Status: {self._status.value}"
        lines = [f"Order #{self._order_id} | Status: {self._status.value}"]
        for item, qty in zip(self._items, self._quantities):
            lines.append(f"  - {item.name} x{qty}  Rs.{item.price * qty:.2f}")
        lines.append(f"  Subtotal: Rs.{self.calculate_subtotal():.2f}")
        lines.append(f"  Tax(5%): Rs.{self.calculate_tax():.2f}")
        lines.append(f"  Total:   Rs.{self.calculate_total():.2f}")
        return "\n".join(lines)

    # ── Serialization ─────────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "order_id": self._order_id,
            "status": self._status.value,
            "items": [
                {"item": item.to_dict(), "qty": qty}
                for item, qty in zip(self._items, self._quantities)
            ],
        }

    @staticmethod
    def from_dict(data: dict) -> "Order":
        from models.menu_item import MenuItem
        order = Order.__new__(Order)
        order._order_id = data["order_id"]
        order._status = OrderStatus(data["status"])
        order._items = [MenuItem.from_dict(e["item"]) for e in data["items"]]
        order._quantities = [e["qty"] for e in data["items"]]
        # keep counter ahead of loaded IDs
        if data["order_id"] >= Order._id_counter:
            Order._id_counter = data["order_id"] + 1
        return order
