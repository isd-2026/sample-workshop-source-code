import sqlite3
from backend.models.db_connect import get_connection

# --------------------- CREATE ---------------------
def add_user(name, email, password,gender, favcol):
    """Insert a new user into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (name, email, password, gender, favcol)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, password, gender, favcol))
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Email '{email}' already exists.") from e
    finally:
        conn.close()

# --------------------- READ (for search) -----------------------
def get_user_by_email(email):
    """Fetch a single user by email."""
    conn = get_connection()
    cursor = conn.cursor()
    # the trailing comma is needed for Python to consider email as a single-item tuple instead of an iterable string
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,)) 
    # fetchone returns a user tuple if user is found and None if the user is not found
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(id):
    """Fetch a single user by id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,)) 
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_users():
    """Fetch all users."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# --------------------- UPDATE ---------------------
def update_user(email, name=None, new_email=None, password=None, gender=None, favcol=None):
    """Update user fields. Only provided fields will be updated."""
    conn = get_connection()
    cursor = conn.cursor()

    fields = []
    values = []

    if name is not None:
        fields.append("name = ?")
        values.append(name)
    if password is not None:
        fields.append("password = ?")
        values.append(password)
    if new_email is not None:
        fields.append("email = ?")
        values.append(new_email)
    if gender is not None:
        fields.append("gender = ?")
        values.append(gender)
    if favcol is not None:
        fields.append("favcol = ?")
        values.append(favcol)

    if not fields:
        return

    values.append(email)

    sql = f"UPDATE users SET {', '.join(fields)} WHERE email = ?"
    cursor.execute(sql, values)
    conn.commit() # if the user is not found, no rows will be updated, no exception is raised
    conn.close()

# --------------------- DELETE ---------------------
def delete_user(user_email):
    """Delete a user by email."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE email = ?", (user_email,))
    conn.commit()
    conn.close()