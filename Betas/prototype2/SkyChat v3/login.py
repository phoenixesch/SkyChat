import tkinter as tk
from tkinter import messagebox
import os
import subprocess

class SkyChatLogin:
    def __init__(self, master):
        self.master = master
        self.master.title("SkyChat Login")
        self.master.geometry("300x200")

        self.label_ip = tk.Label(master, text="Server IP:")
        self.label_ip.pack()
        self.entry_ip = tk.Entry(master)
        self.entry_ip.pack()

        self.label_port = tk.Label(master, text="Server Port:")
        self.label_port.pack()
        self.entry_port = tk.Entry(master)
        self.entry_port.pack()

        self.label_username = tk.Label(master, text="Username:")
        self.label_username.pack()
        self.entry_username = tk.Entry(master)
        self.entry_username.pack()

        self.label_password = tk.Label(master, text="Password:")
        self.label_password.pack()
        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.pack()

        self.button_login = tk.Button(master, text="Login", command=self.login)
        self.button_login.pack()

    def login(self):
        server_ip = self.entry_ip.get()
        server_port = self.entry_port.get()
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not all([server_ip, server_port, username, password]):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            if self.check_credentials(username, password):
                messagebox.showinfo("Success", "Login successful!")
                self.launch_main_menu()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to login: {e}")

    def check_credentials(self, username, password):
        # Path to the database file under the administration folder
        database_file_path = os.path.join("administration", "database_se.kek")

        # Check if the file exists
        if not os.path.exists(database_file_path):
            raise FileNotFoundError("Database file not found")

        # Attempt to open the file and read passwords
        with open(database_file_path, "r") as file:
            for line in file:
                stored_username, stored_password = line.strip().split(":")
                if username == stored_username and password == stored_password:
                    # Username and password match
                    return True
        
        # No matching username and password found
        return False

    def launch_main_menu(self):
        subprocess.Popen(["python", "message/mainmenu.py"])

def main():
    root = tk.Tk()
    app = SkyChatLogin(root)
    root.mainloop()

if __name__ == "__main__":
    main()
