import tkinter as tk
import subprocess
import os

class FullScreenWindow:
    def __init__(self, username):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)  # Make window full screen
        self.root.configure(bg='black')  # Set background color to black

        # Bind Escape key to exit full screen mode
        self.root.bind('<Escape>', self.exit_full_screen)

        # Display welcome message with username
        welcome_message = f"Welcome, {username}!"
        self.welcome_label = tk.Label(self.root, text=welcome_message, font=('Helvetica', 16), fg='white', bg='black')
        self.welcome_label.pack(side='top', pady=20)

        # Create a button for direct messages
        self.direct_messages_button = tk.Button(self.root, text="Direct Messages", command=self.open_direct_messages, bg='blue', fg='white')
        self.direct_messages_button.pack(pady=10)

        # Create a button for chatrooms
        self.chatrooms_button = tk.Button(self.root, text="Chatrooms", command=self.open_chatrooms, bg='green', fg='white')
        self.chatrooms_button.pack(pady=10)

        # Create a button for account settings
        self.account_settings_button = tk.Button(self.root, text="Account Settings", command=self.open_account_settings, bg='orange', fg='white')
        self.account_settings_button.place(relx=1.0, rely=0, anchor='ne', x=-10, y=10)  # Place button in top-right corner

        # Create an exit button
        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_program, bg='red', fg='white')
        self.exit_button.place(relx=1.0, rely=0, anchor='ne', x=-10, y=50)  # Place button in top-right corner

        self.root.mainloop()

    def exit_full_screen(self, event):
        self.root.attributes('-fullscreen', False)
        self.root.destroy()

    def exit_program(self):
        self.root.destroy()

    def open_direct_messages(self):
        # Change directory to 'dms'
        os.chdir('dms')
        # Run mainmenu.py
        subprocess.Popen(["python", "mainmenu.py"])
        # Change directory back to the original location
        os.chdir('..')

    def open_chatrooms(self):
        # Functionality to open chatrooms window can be added here
        print("Chatrooms button clicked.")

    def open_account_settings(self):
        # Open accountsettings.py
        subprocess.Popen(["python", "accountsettings.py"])

if __name__ == "__main__":
    # Assume username is obtained from the login process
    username = "example_user"
    FullScreenWindow(username)
