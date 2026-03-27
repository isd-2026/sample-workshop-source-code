import unittest
from backend.models.db_crud import *
from backend.models.db_connect import get_connection

class TestDBCRUD(unittest.TestCase):
    def setUp(self):
        """Runs before each test: create users table."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                gender TEXT,
                favcol TEXT
            )
        """)
        conn.commit()
        conn.close()

    def test_connection(self):
        """Ensure a connection can be established."""
        conn = None
        try:
            conn = get_connection()
            print("Database connected successfully.")
        finally:
            if conn:
                conn.close()

    def test_add_and_get_user(self):
        """Test inserting and retrieving a user."""
        add_user("Alice", "alice@example.com", "pw", "Female", "Blue")
        user = get_user_by_email("alice@example.com")
        self.assertEqual(user["name"], "Alice")
        self.assertEqual(user["favcol"], "Blue")

    def test_add_user_duplicate_email(self):
        """Adding a user with an existing email should raise ValueError."""
        add_user("Alice", "alice@example.com", "pw", "Female", "Blue")
        with self.assertRaises(ValueError):
            add_user("Alice2", "alice@example.com", "pw", "Female", "Red")

    def test_get_all_users(self):
        """Insert multiple users and fetch all."""
        add_user("Charlie", "c@example.com", "pw", "Male", "Red")
        add_user("Diana", "d@example.com", "pw", "Female", "Purple")
        # returns a list of sqlite3.Row objects
        users = get_all_users()
        self.assertEqual(len(users), 2)
        self.assertEqual({u["name"] for u in users}, {"Charlie", "Diana"})

    def test_update_user(self):
        """Update a user’s details."""
        add_user("Eve", "eve@example.com", "pw", "Female", "Yellow")
        user = get_user_by_email("eve@example.com")

        update_user(user["email"], name="Eve Updated", favcol="Black")
        updated_user = get_user_by_email(user["email"])
        self.assertEqual(updated_user[1], "Eve Updated")
        self.assertEqual(updated_user[5], "Black")

    def test_delete_user(self):
        """Delete a user by ID."""
        add_user("Frank", "frank@example.com", "pw", "Male", "Orange")
        user = get_user_by_email("frank@example.com")

        delete_user(user["email"])
        deleted = get_user_by_email("frank@example.com")
        self.assertIsNone(deleted)

    # tearDown to remove all rows from users table
    def tearDown(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()
        conn.close()


if __name__ == "__main__":
    unittest.main()
