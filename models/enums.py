from enum import Enum


class Category(Enum):
    Drinks = "Drinks"
    FastFood = "Fast Food"
    Desserts = "Desserts"


class OrderStatus(Enum):
    Pending = "Pending"
    Completed = "Completed"
    Cancelled = "Cancelled"
