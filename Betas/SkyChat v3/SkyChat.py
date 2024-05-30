import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import socket
import threading
import subprocess
import hashlib  # For hashing passwords

class ChatClientGUI:
    PRONOUNS = ["He/Him", "She/Her", "They/Them"]  # Pronouns options

    def __init__(self, master):
        self.master = master
        self.master.title("SkyChat Client")

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

        self.pronouns_label = tk.Label(self.master, text="Pronouns:")
        self.pronouns_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.pronouns_combo = ttk.Combobox(self.master, values=self.PRONOUNS)
        self.pronouns_combo.current(0)  # Default selection
        self.pronouns_combo.grid(row=4, column=1, padx=5, pady=5)

        self.connect_button = tk.Button(self.master, text="Connect", command=self.connect_to_server)
        self.connect_button.grid(row=5, column=0, padx=5, pady=5)

        self.login_button = tk.Button(self.master, text="Server Login", command=self.open_server_login)
        self.login_button.grid(row=5, column=1, padx=5, pady=5)

        self.history_button = tk.Button(self.master, text="View History", command=self.view_history)
        self.history_button.grid(row=5, column=2, padx=5, pady=5)

        self.settings_button = tk.Button(self.master, text="Settings", command=self.open_settings_window)
        self.settings_button.grid(row=5, column=3, padx=5, pady=5)

        self.user_history = []
        self.connected = False

    def connect_to_server(self):
        if self.connected:
            messagebox.showerror("Error", "Already connected to the server!")
            return
        server_ip = self.ip_entry.get()
        server_port = self.port_entry.get()
        username = self.username_entry.get()
        pronouns = self.pronouns_combo.get()
        password = self.password_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_ip, int(server_port)))
            self.client_socket.send(f"CONNECT {username} ({pronouns}) {hashed_password}".encode("utf-8"))  # Send username, pronouns, and password hash to server
            response = self.client_socket.recv(1024).decode("utf-8")
            if response == "SUCCESS":
                messagebox.showinfo("Success", "Connected to the server!")
                self.connected = True
                self.open_chat_window()
                threading.Thread(target=self.receive_messages, daemon=True).start()
            else:
                messagebox.showerror("Error", response)
                self.client_socket.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {e}")

    def open_server_login(self):
        subprocess.Popen(["python", "serverlogin.py"])

    def open_chat_window(self):
        self.chat_window = tk.Toplevel(self.master)
        self.chat_window.title("SkyChat")
        self.chat_box = scrolledtext.ScrolledText(self.chat_window, height=20, width=50)
        self.chat_box.pack(padx=10, pady=10)
        self.message_entry = tk.Entry(self.chat_window)
        self.message_entry.pack(padx=10, pady=5)
        self.send_button = tk.Button(self.chat_window, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=5)
        self.update_chat()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            try:
                self.client_socket.send(message.encode("utf-8"))
                self.user_history.append(f"You: {message}")
                self.message_entry.delete(0, tk.END)
                self.update_chat()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send message: {e}")

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = data.decode("utf-8")
                self.user_history.append(f"Server: {message}")  # Show messages from the server
                self.update_chat()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to receive message: {e}")
                break

    def view_history(self):
        history_window = tk.Toplevel(self.master)
        history_window.title("Chat History")
        history_text = scrolledtext.ScrolledText(history_window, height=20, width=50)
        history_text.pack(padx=10, pady=10)
        for msg in self.user_history:
            history_text.insert(tk.END, msg + "\n")

    def update_chat(self):
        self.chat_box.delete(1.0, tk.END)
        for msg in self.user_history:
            self.chat_box.insert(tk.END, msg + "\n")

    def open_settings_window(self):
        subprocess.Popen(["python", "settings.py"])

def main():
    root = tk.Tk()
    app = ChatClientGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# This program was created by SkyNet IT. visit www.skynetit.org for more info. 
# Python Progamming: Skylar Myers (MyersS@SkylarMyersIT.org), Phoenix Eschbach (27PEschbach@SkylarMyersIT.org).
# Javasrcpit Porgamming: Alec P (27PAlex@SkylarMyersIT.org).