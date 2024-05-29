import tkinter as tk
import subprocess
import os

class SettingsWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Settings")
        
        # About label
        self.about_label = tk.Label(self.master, text="About SkyChat\nSkyChat V2 by Skylar Myers")
        self.about_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.ip_label = tk.Label(self.master, text="Server IP:")
        self.ip_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ip_entry = tk.Entry(self.master)
        self.ip_entry.grid(row=1, column=1, padx=5, pady=5)

        # Add Plugin button
        self.plugin_button = tk.Button(self.master, text="Plugin (Coming Soon)", state=tk.DISABLED)
        self.plugin_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Add SkyNet Online Services button
        self.skynet_button = tk.Button(self.master, text="SkyNet Online Services", command=self.open_skynet)
        self.skynet_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Add Apply Settings button
        self.apply_button = tk.Button(self.master, text="Apply Settings", command=self.apply_settings)
        self.apply_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Add Open Terminal button
        self.open_terminal_button = tk.Button(self.master, text="Open Terminal", command=self.open_terminal)
        self.open_terminal_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def apply_settings(self):
        # Implement the functionality to apply settings here
        pass

    def open_terminal(self):
        subprocess.Popen(["python", "terminal.py"])  # Open terminal.py using subprocess

    def open_skynet(self):
        # Change directory to "SkyNet Online Server v1" folder
        os.chdir("SkyNet Online Server v1")
        # Open login.py using subprocess
        subprocess.Popen(["python", "login.py"])

def main():
    root = tk.Tk()
    app = SettingsWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
