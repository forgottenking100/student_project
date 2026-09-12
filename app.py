import sys
from DB_HELP import register_user, authenticate_user

def show_menu():
    print("\n=== SYSTEM MENU ===")
    print("1. Sign Up (Register)")
    print("2. Log In")
    print("3. Exit")
    return input("Choose an option (1-3): ").strip()

def signup_flow():
    print("\n--- Create Account ---")
    username = input("Enter Username: ").strip()
    email = input("Enter Email: ").strip()
    password = input("Enter Password: ").strip()
    
    if not username or not email or not password:
        print("Error: All fields are required.")
        return

    success, message = register_user(username, email, password)
    print(message)

def login_flow():
    print("\n--- User Login ---")
    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()

    success, message = authenticate_user(username, password)
    print(message)
    
    if success:
        user_dashboard(username)

def user_dashboard(username):
    print(f"\nWelcome to your database dashboard, {username}!")
    input("Press Enter to log out...")
    print("Logged out successfully.")

def main():
    while True:
        choice = show_menu()
        if choice == "1":
            signup_flow()
        elif choice == "2":
            login_flow()
        elif choice == "3":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
import sqlite3 as st

DB_FILE = "users.db"

def init_db():
    """Creates the SQLite database and users table if they do not exist."""
    conn = st.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def manual_hash(password):
    """Manually scrambles a password using pure math character shifts."""
    scrambled_chars = []
    shift_key = 7
    
    for i in range(len(password)):
        # Calculate a dynamic mathematical shift per character
        char_code = ord(password[i])
        dynamic_shift = char_code + shift_key + i
        scrambled_chars.append(str(dynamic_shift))
        
    # Join with a delimiter to safely separate values
    return "-".join(scrambled_chars)

def register_user(username, email, password):
    """Saves a new user record into the database."""
    init_db()
    conn = st.connect(DB_FILE)
    cursor = conn.cursor()
    secure_password = manual_hash(password)
    
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, secure_password)
        )
        conn.commit()
        return True, "Registration successful!"
    except st.IntegrityError as e:
        error_msg = str(e)
        if "username" in error_msg:
            return False, "Username already exists."
        elif "email" in error_msg:
            return False, "Email already exists."
        return False, "Username or Email already exists."
    finally:
        conn.close()

def authenticate_user(username, password):
    """Checks user credentials against the stored SQLite database row."""
    init_db()
    conn = st.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return False, "User not found."
        
    # Extract the plain text value out of the query row tuple
    stored_scramble = row[0]
    provided_scramble = manual_hash(password)
    
    if stored_scramble == provided_scramble:
        return True, "Login successful!"
        
    return False, "Invalid password."


