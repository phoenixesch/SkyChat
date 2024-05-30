import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class UserAdministration:
    def __init__(self, master):
        self.master = master
        self.master.title("User Administration")
        self.master.geometry("400x450")  # Set the window size to 400x450 pixels

        self.label = tk.Label(self.master, text="User Administration Panel")
        self.label.pack(pady=20)

        # View User Database Button
        self.view_db_button = tk.Button(self.master, text="View User Database", command=self.view_user_database)
        self.view_db_button.pack(pady=10)

    def get_db_path(self):
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the full path to the database file
        return os.path.join(script_dir, "database_se.kek")

    def view_user_database(self):
        db_path = self.get_db_path()
        if not os.path.exists(db_path):
            messagebox.showerror("Error", "User database file not found!")
            return

        with open(db_path, "r") as db_se_file:
            try:
                self.user_data = json.load(db_se_file)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Error reading user database file!")
                return

        # Create a new window to display user database
        db_window = tk.Toplevel(self.master)
        db_window.title("User Database")
        db_window.geometry("500x500")

        # Treeview to display user data
        self.tree = ttk.Treeview(db_window, columns=("Username", "Last Login Date"), show="headings")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Last Login Date", text="Last Login Date")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Sort users by username and last login date
        sorted_users = sorted(self.user_data.items(), key=lambda item: (item[0], item[1].get("last_login", "")))

        # Insert user data into the treeview
        for username, info in sorted_users:
            last_login = info.get("last_login", "N/A")
            self.tree.insert("", tk.END, values=(username, last_login))

        # Add User Button
        add_user_button = tk.Button(db_window, text="Add User", command=self.add_user)
        add_user_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Delete User Button
        delete_user_button = tk.Button(db_window, text="Delete User", command=self.delete_user)
        delete_user_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def add_user(self):
        # Create a popup window for adding a new user
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New User")
        add_window.geometry("300x250")

        tk.Label(add_window, text="Name:").pack(pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.pack(pady=5)

        tk.Label(add_window, text="Username:").pack(pady=5)
        username_entry = tk.Entry(add_window)
        username_entry.pack(pady=5)

        tk.Label(add_window, text="Password:").pack(pady=5)
        password_entry = tk.Entry(add_window, show="*")
        password_entry.pack(pady=5)

        def save_user():
            name = name_entry.get()
            username = username_entry.get()
            password = password_entry.get()

            if not name or not username or not password:
                messagebox.showerror("Error", "All fields are required!")
                return

            # Add new user to user_data
            if username in self.user_data:
                messagebox.showerror("Error", "Username already exists!")
                return

            self.user_data[username] = {
                "name": name,
                "password": password,
                "last_login": "N/A"
            }

            # Save the updated user data to file
            db_path = self.get_db_path()
            with open(db_path, "w") as db_se_file:
                json.dump(self.user_data, db_se_file)

            messagebox.showinfo("Success", "User added successfully.")
            add_window.destroy()
            self.refresh_treeview()

        tk.Button(add_window, text="Create User", command=save_user).pack(pady=20)

    def delete_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No user selected!")
            return

        username = self.tree.item(selected_item[0], "values")[0]

        if messagebox.askyesno("Confirmation", f"Are you sure you want to delete user '{username}'?"):
            del self.user_data[username]

            # Save the updated user data to file
            db_path = self.get_db_path()
            with open(db_path, "w") as db_se_file:
                json.dump(self.user_data, db_se_file)

            messagebox.showinfo("Success", "User deleted successfully.")
            self.refresh_treeview()

    def refresh_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        sorted_users = sorted(self.user_data.items(), key=lambda item: (item[0], item[1].get("last_login", "")))
        for username, info in sorted_users:
            last_login = info.get("last_login", "N/A")
            self.tree.insert("", tk.END, values=(username, last_login))

def main():
    root = tk.Tk()
    app = UserAdministration(root)
    root.mainloop()

if __name__ == "__main__":
    main()
