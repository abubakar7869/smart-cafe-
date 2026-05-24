"""
PDF Requirement – Task 3 (Advanced):
  Inheritance: Person → Customer, Person → Staff
"""


class Person:
    """Base class for all people in the system."""

    def __init__(self, name: str):
        if not name or not name.strip():
            raise ValueError("Name cannot be empty.")
        self._name = name.strip()

    @property
    def name(self) -> str:
        return self._name

    def __str__(self):
        return f"Person: {self._name}"


class Staff(Person):
    """
    Staff/Admin role.
    PDF Requirement: Staff inherits Person and can manage menu.
    """

    def __init__(self, name: str, staff_id: int):
        super().__init__(name)
        self._staff_id = staff_id

    @property
    def staff_id(self) -> int:
        return self._staff_id

    def manage_menu(self):
        """Placeholder – signals Staff has menu management rights."""
        print(f"[Staff] {self._name} is managing the menu.")

    def __str__(self):
        return f"Staff | ID: {self._staff_id} | Name: {self._name}"


class Customer(Person):
    """
    Customer role.
    PDF Requirement: Customer inherits Person, has unique ID,
    can place orders, and keeps order history.
    """

    _id_counter = 1  # auto-increment unique customer IDs

    def __init__(self, name: str):
        super().__init__(name)
        self._customer_id = Customer._id_counter
        Customer._id_counter += 1
        self._orders = []  # order history

    @property
    def customer_id(self) -> int:
        return self._customer_id

    @property
    def orders(self) -> list:
        return self._orders

    def place_order(self, order):
        """Add an order to this customer's history."""
        self._orders.append(order)
        print(f"[Customer] {self._name} placed Order #{order.order_id}.")

    def show_order_history(self):
        """PDF Requirement: display customer order history."""
        if not self._orders:
            print(f"No order history for {self._name}.")
            return
        print(f"\n=== Order History for {self._name} (ID: {self._customer_id}) ===")
        for order in self._orders:
            print(order)

    def __str__(self):
        return (
            f"Customer | ID: {self._customer_id} | Name: {self._name} "
            f"| Orders: {len(self._orders)}"
        )
