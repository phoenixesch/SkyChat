import tkinter as tk
import subprocess

class AdminMainMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Administration")
        self.master.geometry("300x200")  # Set the window size to 300x200 pixels
        
        self.label = tk.Label(self.master, text="Administration Main Menu")
        self.label.pack(pady=20)
        
        self.user_admin_button = tk.Button(self.master, text="User Administration", command=self.user_admin)
        self.user_admin_button.pack(pady=10)
        
        self.db_admin_button = tk.Button(self.master, text="Database Administration", command=self.db_admin)
        self.db_admin_button.pack(pady=10)
        
        self.footer_label = tk.Label(self.master, text="SkyChat Server", fg="grey")
        self.footer_label.pack(side=tk.BOTTOM, pady=10)
        
    def user_admin(self):
        subprocess.Popen(["python", "administration/useradministration.py"])
        
    def db_admin(self):
        subprocess.Popen(["python", "administration/databaseadministration.py"])

def main():
    root = tk.Tk()
    app = AdminMainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
