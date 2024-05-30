import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading
import subprocess
import re
import json
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
        
        self.admin_button = tk.Button(self.buttons_frame, text="Administration", command=self.open_admin_menu)
        self.admin_button.pack(pady=5)
        
        self.message_entry = tk.Entry(self.master, width=40)
        self.message_entry.pack(padx=10, pady=5)
        self.message_entry.bind("<Return>", self.send_message_on_enter)  # Bind <Return> key to send message
        
        self.send_button = tk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=5)
        
        self.log_box = scrolledtext.ScrolledText(self.master, height=15, width=50)
        self.log_box.pack(padx=10, pady=5)
    
    def start_server(self):
        self.initialize_database_files()
        
        host = "127.0.0.1"
        port = 5555
        self.log_box.insert(tk.END, f"Server listening on {host}:{port}\n")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = []
        self.client_addresses = {}
        threading.Thread(target=self.accept_connections, daemon=True).start()
    
    def initialize_database_files(self):
        admin_folder = "administration"
        db_path = "database.kek"
        db_se_path = "database_se.kek"

        if not os.path.exists(db_path) or not os.path.exists(db_se_path):
            response = messagebox.askyesno("Database Files Missing", "No database files found. Do you want to initialize the database?")
            if response:
                subprocess.Popen(["python", os.path.join(admin_folder, "database administration", "initialize_database.py")])
                return
            else:
                messagebox.showwarning("Database Files Missing", "You must initialize the database for the server to work properly.")
                return

        initialized = False
        self.log_box.insert(tk.END, f"Checking for database files in: {admin_folder}\n")

        if not os.path.exists(db_path):
            with open(db_path, "w") as db_file:
                json.dump({}, db_file)
            self.log_box.insert(tk.END, f"Initialized database.kek at {db_path}\n")
            initialized = True
        
        if not os.path.exists(db_se_path):
            with open(db_se_path, "w") as db_se_file:
                json.dump({}, db_se_file)
            self.log_box.insert(tk.END, f"Initialized database_se.kek at {db_se_path}\n")
            initialized = True

        if initialized:
            self.log_box.insert(tk.END, "Database files have been initialized.\n")
            messagebox.showinfo("Initialization Complete", "Database files have been initialized successfully.")
    
    def accept_connections(self):
        while True:
            client_socket, address = self.server_socket.accept()
            self.clients.append(client_socket)
            self.client_addresses[client_socket] = address
            threading.Thread(target=self.handle_client, args=(client_socket, address), daemon=True).start()
    
    def handle_client(self, client_socket, address):
        username = None
        try:
            credentials = client_socket.recv(1024).decode("utf-8")
            username, password = credentials.split(":", 1)
            
            if not self.authenticate_user(username, password):
                client_socket.send("Invalid credentials. Connection closed.".encode("utf-8"))
                client_socket.close()
                return
            
            self.log_box.insert(tk.END, f"User {username} connected.\n")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode("utf-8")
                self.log_box.insert(tk.END, f"{username}: {message}\n")
                self.handle_command(message)
                self.broadcast_message(f"{username}: {message}")
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            client_socket.close()
            if client_socket in self.client_addresses:
                del self.client_addresses[client_socket]
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            if username:
                self.log_box.insert(tk.END, f"Connection with {username} closed.\n")
            else:
                self.log_box.insert(tk.END, "Connection with unknown user closed.\n")
    
    def authenticate_user(self, username, password):
        admin_folder = "administration"
        db_se_path = os.path.join(admin_folder, "database_se.kek")

        if not os.path.exists(db_se_path):
            return False

        with open(db_se_path, "r") as db_se_file:
            try:
                user_data = json.load(db_se_file)
            except json.JSONDecodeError:
                return False
        
        if username in user_data and user_data[username]["password"] == password:
            return True
        return False
    
    def handle_command(self, message):
        command_pattern = re.compile(r"--(\w+)(?:\s\"([\d\.]+)\")?")
        match = command_pattern.match(message)
        if match:
            command, ip_address = match.groups()
            if command == "whitelistip":
                self.log_box.insert(tk.END, f"Whitelisting IP: {ip_address}\n")
            elif command == "blacklistip":
                self.log_box.insert(tk.END, f"Blacklisting IP: {ip_address}\n")
            elif command == "kickip":
                self.log_box.insert(tk.END, f"Kicking IP: {ip_address}\n")
            elif command == "help":
                self.log_box.insert(tk.END, "Available commands:\n")
                self.log_box.insert(tk.END, "--whitelistip \"<IP address>\": Whitelist an IP address\n")
                self.log_box.insert(tk.END, "--blacklistip \"<IP address>\": Blacklist an IP address\n")
                self.log_box.insert(tk.END, "--kickip \"<IP address>\": Kick an IP address\n")
        else:
            self.log_box.insert(tk.END, "Invalid command format\n")
    
    def broadcast_message(self, message):
        for client_socket in self.clients:
            try:
                client_socket.send(message.encode("utf-8"))
            except Exception as e:
                print(f"Error broadcasting message to {client_socket}: {e}")
    
    def open_settings(self):
        subprocess.Popen(["python", "srvrsettings.py"])
    
    def open_admin_menu(self):
        subprocess.Popen(["python", "administration/mainmenu.py"])
    
    def send_message(self, event=None):
        message = self.message_entry.get()
        self.handle_command(message)
        self.message_entry.delete(0, tk.END)
    
    def send_message_on_enter(self, event): 
        self.send_message()

def main():
    root = tk.Tk()
    app = SkyChatServerAdmin(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# This program was created by SkyNet IT. visit www.skynetit.org for more info. 
# Python Progamming: Skylar Myers (MyersS@SkylarMyersIT.org), Phoenix Eschbach (27PEschbach@SkylarMyersIT.org).
# Javasrcpit Porgamming: Alec P (27PAlex@SkylarMyersIT.org)