"""
PDF Requirement – Task 4 (Expert):
  Exception handling: empty order, invalid input, file errors.
"""


class EmptyOrderError(Exception):
    """Raised when trying to checkout/print an empty order."""
    pass


class ItemNotFoundError(Exception):
    """Raised when a menu item or order item cannot be located."""
    pass


class InvalidInputError(Exception):
    """Raised on bad user input (negative price, empty name, etc.)."""
    pass


class FileError(Exception):
    """Raised when file read/write operations fail."""
    pass
