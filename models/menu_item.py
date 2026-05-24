"""
PDF Requirement – Task 1 (Basic):
  class MenuItem with name, price, category + display()
"""

from models.enums import Category


class MenuItem:
    """Represents a single item on the cafe menu."""

    def __init__(self, name: str, price: float, category: Category, description: str = ""):
        # --- Validation (PDF: error handling) ---
        if not name or not name.strip():
            raise ValueError("MenuItem name cannot be empty.")
        if price <= 0:
            raise ValueError("MenuItem price must be greater than 0.")
        if not isinstance(category, Category):
            raise TypeError(f"category must be a Category enum, got {type(category)}.")

        self._name = name.strip()
        self._price = price
        self._category = category
        self._description = description

    # ---------- properties ----------
    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if value <= 0:
            raise ValueError("Price must be greater than 0.")
        self._price = value

    @property
    def category(self) -> Category:
        return self._category

    @property
    def description(self) -> str:
        return self._description

    # ---------- display ----------
    def display(self):
        """PDF Requirement: display() method on MenuItem."""
        print(
            f"  [{self._category.value}] {self._name:<25} "
            f"Rs.{self._price:>7.2f}"
            + (f"  — {self._description}" if self._description else "")
        )

    def __str__(self):
        return (
            f"{self._name} | {self._category.value} | "
            f"Rs.{self._price:.2f}"
        )

    # ---------- serialization ----------
    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "price": self._price,
            "category": self._category.value,
            "description": self._description,
        }

    @staticmethod
    def from_dict(data: dict) -> "MenuItem":
        return MenuItem(
            name=data["name"],
            price=data["price"],
            category=Category(data["category"]),
            description=data.get("description", ""),
        )
