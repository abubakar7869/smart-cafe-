"""
Smart Cafe Ordering System
Course  : Software Construction and Development Lab
Semester: 5th
Instructor: Ms. Samreen

PDF Coverage:
  Task 1  (20M) – MenuItem & Order classes, add items, display order
  Task 2  (30M) – Quantity support, remove item, total with tax
  Task 3  (30M) – Inheritance (Person→Customer, Person→Staff), file handling
  Task 4  (20M) – Exception handling, search/filter
  Bonus   (⭐)   – Discount system + login system
"""

from models.restaurant import Restaurant
from models.menu_item import MenuItem
from models.menu import Menu
from models.order import Order
from models.enums import Category, OrderStatus
from models.person import Customer, Staff
from models.exceptions import EmptyOrderError, ItemNotFoundError, FileError
from utils.file_handler import save_menu, save_order_receipt
# from utils.auth import login   # ← uncomment to enable bonus login


# ─────────────────────────────────────────────────────────────────────────────
# Helper: print section headers
# ─────────────────────────────────────────────────────────────────────────────
def section(title: str):
    print(f"\n{'━' * 45}")
    print(f"  {title}")
    print('━' * 45)


# ─────────────────────────────────────────────────────────────────────────────
# BONUS: Login (uncomment the login() call below to activate)
# ─────────────────────────────────────────────────────────────────────────────
def demo_login():
    """PDF Bonus: Basic login system."""
    # username, role = login()   # uncomment for interactive login
    # For demo we simulate a successful login:
    username, role = "admin", "staff"
    print(f"[Login] Logged in as '{username}' | Role: {role}")
    return username, role


# ─────────────────────────────────────────────────────────────────────────────
# TASK 3: Demonstrate Inheritance  (Person → Customer / Staff)
# ─────────────────────────────────────────────────────────────────────────────
def demo_inheritance():
    section("TASK 3 – Inheritance: Person → Customer & Staff")

    # Staff (inherits Person)
    staff = Staff(name="Sara", staff_id=101)
    print(staff)
    staff.manage_menu()

    # Customer (inherits Person)
    customer1 = Customer(name="Ali")
    customer2 = Customer(name="Fatima")
    print(customer1)
    print(customer2)

    return customer1, customer2


# ─────────────────────────────────────────────────────────────────────────────
# TASK 1: Menu Management (Dynamic)
# ─────────────────────────────────────────────────────────────────────────────
def demo_menu(restaurant: Restaurant):
    section("TASK 1 – Menu Management (Dynamic)")

    menu = restaurant.menu

    # Add items if menu is empty (loaded from file on startup)
    if not menu.list_items():
        print("[Menu] No saved menu found – creating default items...")

        # ── Drinks ──
        menu.add_item(MenuItem("Coffee",       7.00,  Category.Drinks,   "Hot espresso"))
        menu.add_item(MenuItem("Iced Tea",     5.00,  Category.Drinks,   "Cold black tea with lemon"))
        menu.add_item(MenuItem("Mango Shake",  9.00,  Category.Drinks,   "Fresh mango blended"))

        # ── Fast Food ──
        menu.add_item(MenuItem("Burger",       15.00, Category.FastFood, "Classic beef burger"))
        menu.add_item(MenuItem("Pizza Slice",  12.00, Category.FastFood, "Margherita slice"))
        menu.add_item(MenuItem("French Fries",  8.00, Category.FastFood, "Crispy salted fries"))

        # ── Desserts ──
        menu.add_item(MenuItem("Cheesecake",   22.00, Category.Desserts, "Creamy with strawberry sauce"))
        menu.add_item(MenuItem("Brownie",      10.00, Category.Desserts, "Warm chocolate brownie"))

        # Save menu to menu.txt (PDF 2.5)
        restaurant.save_data()

    # Display categorised menu (PDF 2.1)
    section("=== Smart Cafe – Full Menu ===")
    menu.display()

    # Admin: update a price (PDF 2.1 – update items)
    section("Admin Action – Update Price")
    try:
        menu.update_price("Coffee", Category.Drinks, 8.00)
        print("Price of Coffee updated to Rs.8.00")
    except ValueError as e:
        print(f"[Error] {e}")

    # Admin: remove an item (PDF 2.1 – remove items)
    section("Admin Action – Remove Item")
    try:
        menu.remove_item("Brownie", Category.Desserts)
    except ValueError as e:
        print(f"[Error] {e}")

    print("\nMenu after admin changes:")
    menu.display()


# ─────────────────────────────────────────────────────────────────────────────
# TASK 2: Order System Enhancement
# ─────────────────────────────────────────────────────────────────────────────
def demo_order(restaurant: Restaurant, customer: Customer) -> Order:
    section("TASK 2 – Order System: Multiple Items + Quantity + Tax")

    order = restaurant.create_order()
    print(f"Created Order #{order.order_id} | Status: {order.status.value}")

    # Add items (PDF 2.2 – quantity support)
    restaurant.add_item_to_order(order.order_id, "Coffee",      Category.Drinks,   qty=2)
    restaurant.add_item_to_order(order.order_id, "Burger",      Category.FastFood, qty=1)
    restaurant.add_item_to_order(order.order_id, "Cheesecake",  Category.Desserts, qty=1)
    restaurant.add_item_to_order(order.order_id, "Iced Tea",    Category.Drinks,   qty=3)

    section("Order After Adding Items")
    print(order)

    # Change quantity (PDF 2.2)
    section("Change Iced Tea Quantity to 1")
    restaurant.change_order_item_quantity(order.order_id, "Iced Tea", Category.Drinks, new_quantity=1)
    print(order)

    # Remove item (PDF 2.2 – remove item from order – marked IMPORTANT)
    section("Remove Burger from Order")
    restaurant.remove_item_from_order(order.order_id, "Burger", Category.FastFood)
    print(order)

    # Attach order to customer (PDF 2.3 – order history)
    customer.place_order(order)

    return order


# ─────────────────────────────────────────────────────────────────────────────
# TASK 3: File Handling
# ─────────────────────────────────────────────────────────────────────────────
def demo_file_handling(order: Order, customer: Customer):
    section("TASK 3 – File Handling (menu.txt + orders.txt)")
    try:
        save_order_receipt(order, customer_name=customer.name)
        print("[File] Order receipt appended to data/orders.txt")
    except FileError as e:
        print(f"[FileError] {e}")


# ─────────────────────────────────────────────────────────────────────────────
# TASK 4: Exception Handling
# ─────────────────────────────────────────────────────────────────────────────
def demo_exception_handling(restaurant: Restaurant):
    section("TASK 4 – Exception Handling")

    # 1. Empty order checkout
    print("Test 1: Checkout empty order →")
    empty_order = restaurant.create_order()
    try:
        if empty_order.is_empty():
            raise EmptyOrderError("Order is empty! Cannot checkout.")
    except EmptyOrderError as e:
        print(f"  [EmptyOrderError] {e}")

    # 2. Invalid price
    print("\nTest 2: Create MenuItem with negative price →")
    try:
        bad_item = MenuItem("Ghost Item", -5.0, Category.Drinks)
    except ValueError as e:
        print(f"  [ValueError] {e}")

    # 3. Item not found in order
    print("\nTest 3: Remove item that doesn't exist in order →")
    order = restaurant.create_order()
    try:
        order.remove_item("NonExistentItem")
    except ValueError as e:
        print(f"  [ValueError] {e}")

    # 4. Order not found
    print("\nTest 4: Access order with invalid ID →")
    try:
        restaurant._get_order(9999)
    except ItemNotFoundError as e:
        print(f"  [ItemNotFoundError] {e}")

    # 5. Invalid quantity
    print("\nTest 5: Add item with qty=0 →")
    try:
        order2 = restaurant.create_order()
        restaurant.add_item_to_order(order2.order_id, "Coffee", Category.Drinks, qty=0)
    except ValueError as e:
        print(f"  [ValueError] {e}")


# ─────────────────────────────────────────────────────────────────────────────
# TASK 4: Search & Filter (PDF 2.8)
# ─────────────────────────────────────────────────────────────────────────────
def demo_search_filter(restaurant: Restaurant):
    section("TASK 4 – Search & Filter")

    # Search by name
    keyword = "coffee"
    results = restaurant.search_menu(keyword)
    print(f"Search results for '{keyword}':")
    if results:
        for item in results:
            item.display()
    else:
        print("  No items found.")

    # Filter by category
    print(f"\nFilter by category: {Category.FastFood.value}")
    filtered = restaurant.filter_menu(Category.FastFood)
    if filtered:
        for item in filtered:
            item.display()
    else:
        print("  No items in this category.")


# ─────────────────────────────────────────────────────────────────────────────
# BONUS: Billing with Discount (10% student discount)
# ─────────────────────────────────────────────────────────────────────────────
def demo_billing_with_discount(restaurant: Restaurant, customer: Customer):
    section("BONUS – Billing Receipt with 10% Student Discount")

    order = restaurant.create_order()
    restaurant.add_item_to_order(order.order_id, "Coffee",     Category.Drinks,   qty=2)
    restaurant.add_item_to_order(order.order_id, "Pizza Slice",Category.FastFood, qty=1)
    restaurant.add_item_to_order(order.order_id, "Cheesecake", Category.Desserts, qty=1)

    # PDF Bonus: 10% student discount
    STUDENT_DISCOUNT = 0.10
    restaurant.set_order_status(order.order_id, OrderStatus.Completed)   # set BEFORE printing
    order.print_receipt(customer_name=customer.name, discount=STUDENT_DISCOUNT)
    save_order_receipt(order, customer.name)

    # Show customer order history (PDF 2.3)
    customer.place_order(order)
    customer.show_order_history()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    print("\n" + "★" * 45)
    print("     Smart Cafe Ordering System")
    print("     Software Construction & Development Lab")
    print("★" * 45)

    # ── Bonus: Login (simulated) ──────────────────────────────────────────────
    username, role = demo_login()

    # ── Setup restaurant ──────────────────────────────────────────────────────
    restaurant = Restaurant("Smart Cafe")
    restaurant.load_data()   # Task 3: load menu.txt on startup

    # ── Task 3: Inheritance demo ──────────────────────────────────────────────
    customer1, customer2 = demo_inheritance()

    # ── Task 1: Menu management ───────────────────────────────────────────────
    demo_menu(restaurant)

    # ── Task 2: Order system ──────────────────────────────────────────────────
    order = demo_order(restaurant, customer1)

    # ── Task 3: File handling ─────────────────────────────────────────────────
    demo_file_handling(order, customer1)

    # ── Task 4: Exception handling ────────────────────────────────────────────
    demo_exception_handling(restaurant)

    # ── Task 4: Search & Filter ───────────────────────────────────────────────
    demo_search_filter(restaurant)

    # ── Billing receipt for main order ───────────────────────────────────────
    section("TASK 2 – Final Billing Receipt (Order #1)")
    restaurant.set_order_status(order.order_id, OrderStatus.Completed)
    order.print_receipt(customer_name=customer1.name)

    # ── Bonus: Discount + second customer ────────────────────────────────────
    demo_billing_with_discount(restaurant, customer2)

    # ── Restaurant overview ───────────────────────────────────────────────────
    section("Restaurant Overview")
    print(restaurant)
    print(f"  Total Revenue: Rs.{restaurant.total_revenue():.2f}")


if __name__ == "__main__":
    main()
