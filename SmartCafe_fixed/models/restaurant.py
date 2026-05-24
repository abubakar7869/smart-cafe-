"""
Restaurant – top-level manager class.
Coordinates Menu, Orders, Customers, Staff, File Handling.
"""

from models.menu import Menu
from models.menu_item import MenuItem
from models.order import Order
from models.enums import Category, OrderStatus
from models.exceptions import EmptyOrderError, ItemNotFoundError
from utils.file_handler import save_menu, load_menu, save_order_receipt


class Restaurant:
    def __init__(self, name: str):
        self._name = name
        self._menu = Menu()
        self._orders: list[Order] = []

    @property
    def name(self): return self._name

    @property
    def menu(self): return self._menu

    def load_data(self):
        raw = load_menu()
        for data in raw:
            try:
                self._menu.add_item(MenuItem.from_dict(data))
            except Exception as e:
                print(f"[Load] Skipping item '{data.get('name')}': {e}")

    def save_data(self):
        save_menu(self._menu.list_items())

    def create_order(self) -> Order:
        order = Order()
        self._orders.append(order)
        return order

    def add_item_to_order(self, order_id: int, item_name: str,
                          category: Category, qty: int = 1):
        order = self._get_order(order_id)
        item = self._menu.get_item(item_name, category)
        order.add_item(item, qty)

    def remove_item_from_order(self, order_id: int, item_name: str,
                               category: Category):
        order = self._get_order(order_id)
        order.remove_item(item_name, category)

    def change_order_item_quantity(self, order_id: int, item_name: str,
                                   category: Category, new_quantity: int):
        order = self._get_order(order_id)
        order.change_quantity(item_name, category, new_quantity)

    def set_order_status(self, order_id: int, new_status: OrderStatus):
        order = self._get_order(order_id)
        order.status = new_status

    def checkout_order(self, order_id: int, customer_name: str = "Guest",
                       discount: float = 0.0):
        order = self._get_order(order_id)
        if order.is_empty():
            raise EmptyOrderError("Order is empty! Add items before checkout.")
        order.print_receipt(customer_name=customer_name, discount=discount)
        order.status = OrderStatus.Completed
        save_order_receipt(order, customer_name)

    def total_revenue(self) -> float:
        return round(sum(o.calculate_total()
                         for o in self._orders
                         if o.status == OrderStatus.Completed), 2)

    def search_menu(self, keyword: str) -> list:
        return self._menu.search_by_name(keyword)

    def filter_menu(self, category: Category) -> list:
        return self._menu.filter_by_category(category)

    def _get_order(self, order_id: int) -> Order:
        for order in self._orders:
            if order.order_id == order_id:
                return order
        raise ItemNotFoundError(f"Order #{order_id} not found.")

    def __str__(self):
        lines = [
            f"\n{'=' * 40}",
            f"  {self._name}",
            f"{'=' * 40}",
            f"  Total Orders : {len(self._orders)}",
            f"  Revenue      : Rs.{self.total_revenue():.2f}",
            f"{'=' * 40}",
        ]
        return "\n".join(lines)
