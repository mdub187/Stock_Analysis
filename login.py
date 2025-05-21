# login.py
# import customtkinter as ctk
# import bcrypt
from __imports__ import bcr, CTk
from revive import run_main_app  # Import the new main app function

# Configure theme
CTk.set_appearance_mode("Dark")
CTk.set_default_color_theme("blue")

# Store a fixed hashed password for "mypassword"
stored_user = {
    "username": "user1",
    "password_hash": bcr.hashpw(b"mypassword", bcr.gensalt())
}

# Authentication logic
def authenticate(username_input, password_input):
    if username_input == stored_user["username"]:
        return bcr.checkpw(password_input.encode(), stored_user["password_hash"])
    return False

# Login window
def login_window():
    root = CTk.CTk()
    root.geometry("400x300")
    root.title("Login")

    CTk.CTkLabel(root, text="Username:").pack(pady=(20, 5))
    username_entry = CTk.CTkEntry(root)
    username_entry.pack(pady=5)

    CTk.CTkLabel(root, text="Password:").pack(pady=(10, 5))
    password_entry = CTk.CTkEntry(root, show="*")
    password_entry.pack(pady=5)

    def on_login():
        username = username_entry.get()
        password = password_entry.get()
        if authenticate(username, password):
            root.destroy()
            run_main_app()  # Run main app after successful login
        else:
            CTk.CTkLabel(root, text="Invalid username or password", text_color="red").pack(pady=10)

    CTk.CTkButton(root, text="Login", command=on_login).pack(pady=20)
    root.mainloop()

# Entry point
if __name__ == "__main__":
    login_window()
