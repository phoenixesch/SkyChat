import tkinter as tk

class DirectMessagesWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Direct Messages")
        
        # Set the size and position of the window
        window_width = 600
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create widgets for the direct messages window (add your widgets here)

        self.root.mainloop()

if __name__ == "__main__":
    DirectMessagesWindow()
