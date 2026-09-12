from ast import main
import streamlit as st
from DB_HELP import create_table, add_student, verify_student


def main():
    create_table()
    st.title("Student Login System")
    choice = st.sidebar.selectbox("Select an option", ["Login", "Register"])
    if choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username and password:
                if verify_student(username, password):
                    st.success("You have successfully logged in!")
                else:
                    st.warning("Invalid username or password. Please try again.")
    elif choice == "Register":
        st.subheader("Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")    
        if st.button("Register"):
            if username and password:
                if add_student(username, password):
                    st.success("You have successfully registered!")
                else:
                    st.warning("Username already exists. Please choose a different username.")

if __name__ == "__main__":
    main()