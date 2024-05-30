import tkinter as tk
from tkinter import messagebox, ttk
import socket

class ServerLoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Server Login")

        self.ip_label = tk.Label(self.master, text="Server IP:")
        self.ip_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ip_entry = tk.Entry(self.master)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)

        self.port_label = tk.Label(self.master, text="Server Port:")
        self.port_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.port_entry = tk.Entry(self.master)
        self.port_entry.grid(row=1, column=1, padx=5, pady=5)

        self.username_label = tk.Label(self.master, text="Username:")
        self.username_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.username_entry = tk.Entry(self.master)
        self.username_entry.grid(row=2, column=1, padx=5, pady=5)

        self.password_label = tk.Label(self.master, text="Password:")
        self.password_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.grid(row=3, column=1, padx=5, pady=5)

        self.login_button = tk.Button(self.master, text="Login", command=self.login)
        self.login_button.grid(row=4, column=0, padx=5, pady=5)

        self.signup_button = tk.Button(self.master, text="Signup", command=self.signup)
        self.signup_button.grid(row=4, column=1, padx=5, pady=5)

    def check_server_online(self, server_ip, server_port):
        try:
            socket.create_connection((server_ip, int(server_port)), timeout=2)
            return True
        except OSError:
            return False

    def login(self):
        server_ip = self.ip_entry.get()
        server_port = self.port_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if the SkyChat Server is online
        if not self.check_server_online(server_ip, server_port):
            messagebox.showerror("Error", "SkyChat Server is not online!")
            return

        # Check username and password against the database
        # Replace this with your database checking logic
        if username == "admin" and password == "admin":
            messagebox.showinfo("Success", "Login Successful!")
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def signup(self):
        # Add signup functionality here
        messagebox.showinfo("Sign Up", "Sign Up feature will be implemented soon!")

def main():
    root = tk.Tk()
    app = ServerLoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
