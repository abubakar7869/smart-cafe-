# SmartCafe_fixed

A simple Python CLI demo for a small cafe system. Implements OOP models for menu items, menu management, orders, customers/staff, and file-based persistence for demo/teaching purposes.

## Features
- Menu management: add, remove, update, search and display menu items
- Order lifecycle: create order, add/remove items, compute subtotal/tax/total, print/save receipt
- Person model with inheritance: `Person` → `Staff`, `Customer` (order history)
- File-based persistence: menu and receipts saved to `data/` via `utils/file_handler.py`
- Custom exceptions and enums for robust demo behavior

## Project structure

- `main.py` — demo CLI script showing typical flows (login simulation, menu CRUD, ordering, checkout, receipt saving)
- `data/`
  - `menu.txt` — persisted menu storage used by the app
  - `orders.txt` — persisted order/receipt storage (if used)
- `models/` — domain models
  - `enums.py` — `Category`, `OrderStatus`
  - `exceptions.py` — `EmptyOrderError`, `ItemNotFoundError`, `InvalidInputError`, `FileError`
  - `menu_item.py` — `MenuItem` model with validation and (de)serialization
  - `menu.py` — `Menu` class for managing `MenuItem`s
  - `order.py` — `Order` class for order lifecycle and billing
  - `person.py` — `Person`, `Staff`, `Customer` classes
  - `restaurant.py` — orchestrates menu, orders, and revenue tracking
- `utils/`
  - `file_handler.py` — `save_menu`, `load_menu`, `save_order_receipt` helpers (file-based persistence)

## Installation

Requires Python 3.8+. No external dependencies.

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Run the demo:

```powershell
python main.py
```

## Usage notes
- The `main.py` script demonstrates the functionality and is a starting point for exploring the code.
- Data files are stored under `data/`. Modifying them directly may change application state.
- Exceptions from `models/exceptions.py` are raised for invalid operations — see source for exact behavior.

## Screenshot
![Smart Cafe demo screenshot](screenshots/smart-cafe-demo.png)

The screenshot above shows the CLI output for menu management and admin actions such as updating item prices and removing menu items. Add your screenshot file at `screenshots/smart-cafe-demo.png` to display it in the README.

## Developer notes
- Follow the OOP patterns in `models/` when extending features.
- For persistent storage changes, edit `utils/file_handler.py` to migrate from flat-file to JSON/DB.
- Tax, receipt formatting, and serialization live in `models/order.py` and `utils/file_handler.py`.

## License
This repository contains instructional/demo code. No license specified.
