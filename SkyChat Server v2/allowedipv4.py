import tkinter as tk
from tkinter import messagebox

class AllowedIPv4:
    def __init__(self, master, sky_server_ip):
        self.master = master
        self.master.title("Allowed IPv4 Addresses")
        self.sky_server_ip = sky_server_ip

        self.blocked_ips = []

        self.listbox = tk.Listbox(self.master)
        self.listbox.pack(padx=10, pady=10)

        self.block_entry = tk.Entry(self.master)
        self.block_entry.pack(padx=10, pady=5)

        self.block_button = tk.Button(self.master, text="Block IPv4", command=self.block_ipv4)
        self.block_button.pack(padx=10, pady=5)

        self.apply_button = tk.Button(self.master, text="Apply", command=self.apply_changes)
        self.apply_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.cancel_button = tk.Button(self.master, text="Cancel", command=self.master.destroy)
        self.cancel_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def block_ipv4(self):
        ip_address = self.block_entry.get()
        if ip_address and ip_address not in self.blocked_ips:
            if ip_address == self.sky_server_ip:
                messagebox.showwarning("Warning", "Cannot block connection from Sky server.")
            else:
                self.blocked_ips.append(ip_address)
                self.listbox.insert(tk.END, ip_address)
                self.block_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a valid IPv4 address.")

    def apply_changes(self):
        # Here you can save the blocked IPs to a file or perform any other action needed
        messagebox.showinfo("Success", "Changes applied successfully.")
        self.master.destroy()

def main():
    # Simulate getting Sky server IP from SkyServer.py
    sky_server_ip = "192.168.1.100"  # Example IP address, replace with actual IP from SkyServer.py

    root = tk.Tk()
    app = AllowedIPv4(root, sky_server_ip)
    root.mainloop()

if __name__ == "__main__":
    main()
