import tkinter as tk

class AccountSettingsWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Account Settings")
        
        # Set the size and position of the window
        window_width = 400
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create widgets for the account settings window (add your widgets here)

        self.root.mainloop()

if __name__ == "__main__":
    AccountSettingsWindow()
