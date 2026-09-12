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
    print(f"\nWelcome to your dashboard, {username}!")
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

