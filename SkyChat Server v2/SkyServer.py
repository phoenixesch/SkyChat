import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import subprocess
import re

class SkyChatServerAdmin:
    def __init__(self, master):
        self.master = master
        self.master.title("SkyChat Server v2.0 Admin")

        # Create buttons frame
        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.start_button = tk.Button(self.buttons_frame, text="Start Server", command=self.start_server)
        self.start_button.pack(pady=5)

        self.settings_button = tk.Button(self.buttons_frame, text="Settings", command=self.open_settings)
        self.settings_button.pack(pady=5)

        self.message_entry = tk.Entry(self.master, width=40)
        self.message_entry.pack(padx=10, pady=5)
        self.message_entry.bind("<Return>", self.send_message_on_enter)  # Bind <Return> key to send message

        self.send_button = tk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=5)

        self.log_box = scrolledtext.ScrolledText(self.master, height=15, width=50)
        self.log_box.pack(padx=10, pady=5)

    def start_server(self):
        host = "127.0.0.1"  # Change this to your desired host IP
        port = 5555

        self.log_box.insert(tk.END, f"Server listening on {host}:{port}\n")

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)

        self.clients = []
        self.client_addresses = {}

        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while True:
            client_socket, address = self.server_socket.accept()
            self.clients.append(client_socket)
            self.client_addresses[client_socket] = address
            threading.Thread(target=self.handle_client, args=(client_socket, address), daemon=True).start()

    def handle_client(self, client_socket, address):
        try:
            username = client_socket.recv(1024).decode("utf-8")
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
            del self.client_addresses[client_socket]
            self.clients.remove(client_socket)
            self.log_box.insert(tk.END, f"Connection with {username} closed.\n")

    def handle_command(self, message):
        command_pattern = re.compile(r"--(\w+)(?:\s\"([\d\.]+)\")?")
        match = command_pattern.match(message)
        if match:
            command, ip_address = match.groups()
            if command == "whitelistip":
                self.log_box.insert(tk.END, f"Whitelisting IP: {ip_address}\n")
                # Implement whitelist IP logic here
            elif command == "blacklistip":
                self.log_box.insert(tk.END, f"Blacklisting IP: {ip_address}\n")
                # Implement blacklist IP logic here
            elif command == "kickip":
                self.log_box.insert(tk.END, f"Kicking IP: {ip_address}\n")
                # Implement kick IP logic here
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

    def send_message(self, event=None):  # Modified to accept event argument
        self.handle_command(self.message_entry.get())
        self.message_entry.delete(0, tk.END)

    def send_message_on_enter(self, event):  # Method triggered when Enter key is pressed
        self.send_message()

def main():
    root = tk.Tk()
    app = SkyChatServerAdmin(root)
    root.mainloop()

if __name__ == "__main__":
    main()
