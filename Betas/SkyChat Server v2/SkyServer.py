import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import socket
import threading
import subprocess
import re
import sqlite3
import os

class SkyChatServerAdmin:
    def __init__(self, master):
        self.master = master
        self.master.title("SkyChat Server v2.0 Admin")
        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.start_button = tk.Button(self.buttons_frame, text="Start Server", command=self.start_server)
        self.start_button.pack(pady=5)
        self.settings_button = tk.Button(self.buttons_frame, text="Settings", command=self.open_settings)
        self.settings_button.pack(pady=5)
        self.add_user_button = tk.Button(self.buttons_frame, text="Add new user to database", command=self.add_new_user)
        self.add_user_button.pack(pady=5)
        self.message_entry = tk.Entry(self.master, width=40)
        self.message_entry.pack(padx=10, pady=5)
        self.message_entry.bind("<Return>", self.send_message_on_enter)  # Bind <Return> key to send message
        self.send_button = tk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=5)
        self.log_box = scrolledtext.ScrolledText(self.master, height=15, width=50)
        self.log_box.pack(padx=10, pady=5)

        self.db_file = "database.kek"
        self.db_file_se = "database_se.kek"
        self.initialize_database()
        self.initialize_secondary_database()
        
    def initialize_database(self):
        """Initialize the primary database and create tables if they don't exist."""
        if not os.path.exists(self.db_file):
            self.log_box.insert(tk.END, "Creating primary database file...\n")
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                username TEXT PRIMARY KEY,
                                ip_address TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS whitelist (
                                ip_address TEXT PRIMARY KEY)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS blacklist (
                                ip_address TEXT PRIMARY KEY)''')
        self.conn.commit()

    def initialize_secondary_database(self):
        """Initialize the secondary database and create tables if they don't exist."""
        if not os.path.exists(self.db_file_se):
            self.log_box.insert(tk.END, "Creating secondary database file...\n")
        self.conn_se = sqlite3.connect(self.db_file_se)
        self.cursor_se = self.conn_se.cursor()
        self.cursor_se.execute('''CREATE TABLE IF NOT EXISTS additional_info (
                                    info_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    info_text TEXT)''')
        self.conn_se.commit()

    def start_server(self):
        host = "127.0.0.1"
        port = 5555
        self.log_box.insert(tk.END, f"Server listening on {host}:{port}\n")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = []
        self.client_addresses = {}
        self.usernames = set()  # Set to track active usernames
        self.whitelist = set(row[0] for row in self.cursor.execute("SELECT ip_address FROM whitelist"))
        self.blacklist = set(row[0] for row in self.cursor.execute("SELECT ip_address FROM blacklist"))
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while True:
            try:
                client_socket, address = self.server_socket.accept()
                if address[0] in self.blacklist:
                    client_socket.close()
                    self.log_box.insert(tk.END, f"Rejected connection from blacklisted IP {address[0]}\n")
                else:
                    threading.Thread(target=self.authenticate_client, args=(client_socket, address), daemon=True).start()
            except Exception as e:
                self.log_box.insert(tk.END, f"Error accepting connections: {e}\n")

    def authenticate_client(self, client_socket, address):
        try:
            username = client_socket.recv(1024).decode("utf-8")
            if username in self.usernames:
                self.log_box.insert(tk.END, f"Rejected duplicate username: {username} from {address[0]}\n")
                client_socket.close()
            else:
                self.usernames.add(username)
                self.clients.append(client_socket)
                self.client_addresses[client_socket] = address
                self.cursor.execute("INSERT OR IGNORE INTO users (username, ip_address) VALUES (?, ?)", (username, address[0]))
                self.conn.commit()
                self.log_box.insert(tk.END, f"User {username} connected from {address[0]}.\n")
                threading.Thread(target=self.handle_client, args=(client_socket, address, username), daemon=True).start()
        except Exception as e:
            self.log_box.insert(tk.END, f"Error during authentication: {e}\n")

    def handle_client(self, client_socket, address, username):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode("utf-8")
                self.log_box.insert(tk.END, f"{username}: {message}\n")
                self.handle_command(message, client_socket, address)
                self.broadcast_message(f"{username}: {message}", client_socket)
        except Exception as e:
            self.log_box.insert(tk.END, f"Error with client {address[0]}: {e}\n")
        finally:
            client_socket.close()
            del self.client_addresses[client_socket]
            self.clients.remove(client_socket)
            self.usernames.remove(username)
            self.log_box.insert(tk.END, f"Connection with {username} closed.\n")

    def handle_command(self, message, client_socket, address):
        command_pattern = re.compile(r"--(\w+)(?:\s\"([\d\.]+)\")?")
        match = command_pattern.match(message)
        if match:
            command, ip_address = match.groups()
            if command == "whitelistip":
                self.whitelist.add(ip_address)
                self.cursor.execute("INSERT OR IGNORE INTO whitelist (ip_address) VALUES (?)", (ip_address,))
                self.conn.commit()
                self.log_box.insert(tk.END, f"Whitelisted IP: {ip_address}\n")
            elif command == "blacklistip":
                self.blacklist.add(ip_address)
                self.cursor.execute("INSERT OR IGNORE INTO blacklist (ip_address) VALUES (?)", (ip_address,))
                self.conn.commit()
                self.log_box.insert(tk.END, f"Blacklisted IP: {ip_address}\n")
            elif command == "kickip":
                self.kick_ip(ip_address)
            elif command == "help":
                self.log_box.insert(tk.END, "Available commands:\n")
                self.log_box.insert(tk.END, "--blacklistip \"<IP address>\": Blacklist an IP address\n")
                self.log_box.insert(tk.END, "--kickip \"<IP address>\": Kick an IP address\n")
        else:
            self.log_box.insert(tk.END, "Invalid command format\n")

    def kick_ip(self, ip_address):
        for client_socket, addr in list(self.client_addresses.items()):
            if addr[0] == ip_address:
                client_socket.close()
                self.clients.remove(client_socket)
                del self.client_addresses[client_socket]
                self.log_box.insert(tk.END, f"Kicked IP: {ip_address}\n")
                break

    def broadcast_message(self, message, from_socket=None):
        for client_socket in self.clients:
            if client_socket != from_socket:
                try:
                    client_socket.send(message.encode("utf-8"))
                except Exception as e:
                    self.log_box.insert(tk.END, f"Error broadcasting message to {client_socket}: {e}\n")

    def open_settings(self):
        subprocess.Popen(["python", "srvrsettings.py"])

    def send_message(self):
        message = self.message_entry.get()
        self.handle_command(message, None, None)
        self.message_entry.delete(0, tk.END)

    def send_message_on_enter(self, event): 
        self.send_message()

    def add_new_user(self):
        username = simpledialog.askstring("Add New User", "Enter username:")
        password = simpledialog.askstring("Add New User", "Enter password:", show='*')
        if username and password:
            try:
                self.cursor_se.execute("INSERT INTO additional_info (info_text) VALUES (?)", (f"Username: {username}, Password: {password}",))
                self.conn_se.commit()
                messagebox.showinfo("Success", "New user added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add new user: {e}")

def main():
    root = tk.Tk()
    app = SkyChatServerAdmin(root)
    root.mainloop()

if __name__ == "__main__":
    main()