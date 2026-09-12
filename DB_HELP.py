import json
import os
import hashlib

DB_FILE = "users.json"

def init_db():
    """Creates the JSON file database if it doesn't exist."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)

def hash_password(password):
    """Secures the password using standard SHA-256 hashing."""
    salt = "some_secure_unique_salt_string"
    salted_pass = password + salt
    return hashlib.sha256(salted_pass.encode()).hexdigest()

def register_user(username, email, password):
    """Saves user data if the username does not already exist."""
    init_db()
    
    with open(DB_FILE, "r") as f:
        users = json.load(f)
        
    if username in users:
        return False, "Username already exists."
        
    # Check if email is already taken
    for user_data in users.values():
        if user_data["email"] == email:
            return False, "Email already exists."
            
    # Save the user with a hashed password
    users[username] = {
        "email": email,
        "password": hash_password(password)
    }
    
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)
        
    return True, "Registration successful!"

def authenticate_user(username, password):
    """Checks credentials against the stored password hash."""
    init_db()
    
    with open(DB_FILE, "r") as f:
        users = json.load(f)
        
    if username not in users:
        return False, "User not found."
        
    stored_hash = users[username]["password"]
    provided_hash = hash_password(password)
    
    if stored_hash == provided_hash:
        return True, "Login successful!"
        
    return False, "Invalid password."
