"""
PDF Bonus Feature: Basic Login System (username/password).
Keeps credentials in memory for simplicity.
"""

USERS = {
    "admin": {"password": "admin123", "role": "staff"},
    "customer1": {"password": "pass123", "role": "customer"},
}


def login() -> tuple[str, str]:
    """
    Returns (username, role) if login succeeds.
    PDF Bonus: login system (basic username/password).
    """
    print("\n" + "=" * 40)
    print("       Smart Cafe – Login")
    print("=" * 40)
    attempts = 3
    while attempts > 0:
        username = input("  Username: ").strip()
        password = input("  Password: ").strip()
        user = USERS.get(username)
        if user and user["password"] == password:
            print(f"\n  ✓ Welcome, {username}! Role: {user['role']}\n")
            return username, user["role"]
        attempts -= 1
        print(f"  ✗ Invalid credentials. {attempts} attempt(s) left.")
    raise PermissionError("Too many failed login attempts. Access denied.")
