import tkinter as tk
from tkinter import messagebox, ttk
import subprocess

class ServerSettings:
    def __init__(self, master):
        self.master = master
        self.master.title("Server Settings")
        self.about_label = tk.Label(self.master, text="Skychat Server v2.0")
        self.about_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.settings_frame = tk.Frame(self.master)
        self.settings_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.ip_label = tk.Label(self.settings_frame, text="Server IP:")
        self.ip_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ip_entry = tk.Entry(self.settings_frame)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)
        self.port_label = tk.Label(self.settings_frame, text="Server Port:")
        self.port_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.port_entry = tk.Entry(self.settings_frame)
        self.port_entry.grid(row=1, column=1, padx=5, pady=5)
        self.username_label = tk.Label(self.settings_frame, text="Username:")
        self.username_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.username_entry = tk.Entry(self.settings_frame)
        self.username_entry.grid(row=2, column=1, padx=5, pady=5)
        self.pronouns_label = tk.Label(self.settings_frame, text="Pronouns:")
        self.pronouns_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.pronouns_combo = ttk.Combobox(self.settings_frame, values=["He/Him", "She/Her", "They/Them"])
        self.pronouns_combo.current(0)
        self.pronouns_combo.grid(row=3, column=1, padx=5, pady=5)
        self.allowed_ips_button = tk.Button(self.master, text="Allowed IPs", command=self.open_allowed_ips)
        self.allowed_ips_button.grid(row=2, column=0, padx=5, pady=5)
        self.check_updates_button = tk.Button(self.master, text="Check for Updates", command=self.check_for_updates)
        self.check_updates_button.grid(row=2, column=1, padx=5, pady=5)
        self.apply_button = tk.Button(self.master, text="Apply Settings", command=self.apply_settings)
        self.apply_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    def apply_settings(self):
        server_ip = self.ip_entry.get()
        server_port = self.port_entry.get()
        username = self.username_entry.get()
        pronouns = self.pronouns_combo.get()
        save_settings(server_ip, server_port, username, pronouns)
        messagebox.showinfo("Success", "Settings applied and saved.")
    def open_allowed_ips(self):
        subprocess.Popen(["python", "allowedipv4.py"])
    def check_for_updates(self):
        messagebox.showinfo("Feature Disabled", "The update-checking feature is currently disabled.")
def save_settings(server_ip, server_port, username, pronouns):
    with open("configs/settings.txt", "w") as f:
        f.write(f"Server IP: {server_ip}\n")
        f.write(f"Server Port: {server_port}\n")
        f.write(f"Username: {username}\n")
        f.write(f"Pronouns: {pronouns}\n")
def main():
    root = tk.Tk()
    app = ServerSettings(root)
    root.mainloop()
if __name__ == "__main__":
    main()
