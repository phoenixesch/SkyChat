import tkinter as tk
from tkinter import messagebox
import os
import json

class DatabaseAdmin:
    def __init__(self, master):
        self.master = master
        self.master.title("Database Administration")
        self.master.geometry("300x350")  # Set the window size to 300x350 pixels

        self.label = tk.Label(self.master, text="Database Administration Panel")
        self.label.pack(pady=20)

        # Initialize Database Button
        self.init_db_button = tk.Button(self.master, text="Initialize Database", command=self.initialize_database)
        self.init_db_button.pack(pady=10)

        # Label to show the path of the database files
        self.path_label = tk.Label(self.master, text="", fg="blue")
        self.path_label.pack(pady=5)

        # Danger Zone Frame
        self.danger_zone_frame = tk.LabelFrame(self.master, text="Danger Zone", fg="red", padx=10, pady=10)
        self.danger_zone_frame.pack(pady=10, fill="both", expand="yes")

        # Reset Database Button
        self.reset_db_button = tk.Button(self.danger_zone_frame, text="Reset Database", command=self.reset_database)
        self.reset_db_button.pack(pady=5)

        # Delete Database Button
        self.delete_db_button = tk.Button(self.danger_zone_frame, text="Delete Database", command=self.delete_database)
        self.delete_db_button.pack(pady=5)

        # Footer Label
        self.footer_label = tk.Label(self.master, text="SkyChat Server", fg="grey")
        self.footer_label.pack(side=tk.BOTTOM, pady=10)

    def initialize_database(self):
        database_dir = "administration"
        os.makedirs(database_dir, exist_ok=True)

        server_settings = {}
        user_login_info = {}

        db_file_path = os.path.join(database_dir, "database.kek")
        db_se_file_path = os.path.join(database_dir, "database_se.kek")

        with open(db_file_path, "w") as db_file:
            json.dump(server_settings, db_file)

        with open(db_se_file_path, "w") as db_se_file:
            json.dump(user_login_info, db_se_file)

        self.path_label.config(text=f"Database files saved at: {os.path.abspath(database_dir)}")
        messagebox.showinfo("Initialization", "Database initialized successfully.")

    def reset_database(self):
        if self.confirm_action("reset"):
            self.initialize_database()

    def delete_database(self):
        if self.confirm_action("delete"):
            db_file_path = os.path.join("administration", "database.kek")
            db_se_file_path = os.path.join("administration", "database_se.kek")

            if os.path.exists(db_file_path):
                os.remove(db_file_path)
            if os.path.exists(db_se_file_path):
                os.remove(db_se_file_path)
            messagebox.showinfo("Deletion", "Database deleted successfully.")
            self.path_label.config(text="")

    def confirm_action(self, action):
        confirmation_count = 4
        for _ in range(confirmation_count):
            response = messagebox.askyesno("Confirmation", f"Are you sure you want to {action} the database? You have {confirmation_count} chances to go back.")
            if not response:
                messagebox.showinfo("Aborted", f"{action.capitalize()} action aborted.")
                return False
            confirmation_count -= 1
        return True

def main():
    root = tk.Tk()
    app = DatabaseAdmin(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# This program was created by SkyNet IT
