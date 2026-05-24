"""
PDF Requirement – Task 1 & Task 4:
  Menu management: add, remove, update, display (categorised),
  search by name, filter by category.
"""

from models.menu_item import MenuItem
from models.enums import Category


class Menu:
    """Manages the cafe's collection of MenuItems."""

    def __init__(self):
        self._items: list[MenuItem] = []

    # ── Add ──────────────────────────────────────────────────────────────────
    def add_item(self, item: MenuItem):
        """PDF Requirement (Admin/Staff): add new item."""
        if not isinstance(item, MenuItem):
            raise TypeError("Expected a MenuItem instance.")
        # prevent duplicates by name + category
        if self._find(item.name, item.category):
            raise ValueError(f"'{item.name}' already exists in {item.category.value}.")
        self._items.append(item)
        print(f"[Menu] '{item.name}' added to {item.category.value}.")

    # ── Remove ───────────────────────────────────────────────────────────────
    def remove_item(self, name: str, category: Category):
        """PDF Requirement (Admin/Staff): remove item."""
        item = self._find(name, category)
        if not item:
            raise ValueError(f"'{name}' not found in {category.value}.")
        self._items.remove(item)
        print(f"[Menu] '{name}' removed from {category.value}.")

    # ── Update price ──────────────────────────────────────────────────────────
    def update_price(self, name: str, category: Category, new_price: float):
        """PDF Requirement (Admin/Staff): update item price."""
        item = self._find(name, category)
        if not item:
            raise ValueError(f"'{name}' not found in {category.value}.")
        item.price = new_price
        print(f"[Menu] '{name}' price updated to Rs.{new_price:.2f}.")

    # ── Display categorised ───────────────────────────────────────────────────
    def display(self):
        """PDF Requirement: display categorised menu (Drinks, Fast Food, Desserts)."""
        if not self._items:
            print("  [Menu is empty]")
            return
        for cat in Category:
            cat_items = [i for i in self._items if i.category == cat]
            if cat_items:
                print(f"\n  ── {cat.value} ──")
                for item in cat_items:
                    item.display()

    def list_items(self) -> list[MenuItem]:
        return list(self._items)

    # ── Search by name (PDF Task 4) ───────────────────────────────────────────
    def search_by_name(self, keyword: str) -> list[MenuItem]:
        """PDF Requirement: search item by name."""
        keyword = keyword.lower().strip()
        results = [i for i in self._items if keyword in i.name.lower()]
        return results

    # ── Filter by category (PDF Task 4) ──────────────────────────────────────
    def filter_by_category(self, category: Category) -> list[MenuItem]:
        """PDF Requirement: filter by category."""
        return [i for i in self._items if i.category == category]

    # ── Internal helper ───────────────────────────────────────────────────────
    def _find(self, name: str, category: Category):
        for item in self._items:
            if item.name.lower() == name.lower() and item.category == category:
                return item
        return None

    def get_item(self, name: str, category: Category):
        item = self._find(name, category)
        if not item:
            raise ValueError(f"'{name}' not found in {category.value}.")
        return item

    # ── Serialization ─────────────────────────────────────────────────────────
    def to_dict(self) -> list:
        return [i.to_dict() for i in self._items]

    def from_dict(self, data: list):
        from models.menu_item import MenuItem
        self._items = [MenuItem.from_dict(d) for d in data]

    def __str__(self):
        if not self._items:
            return "  [Menu is empty]"
        lines = [""]
        for cat in Category:
            cat_items = [i for i in self._items if i.category == cat]
            if cat_items:
                lines.append(f"  ── {cat.value} ──")
                for item in cat_items:
                    lines.append(
                        f"    {item.name:<25} Rs.{item.price:>7.2f}"
                    )
        return "\n".join(lines)
