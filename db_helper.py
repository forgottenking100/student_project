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


