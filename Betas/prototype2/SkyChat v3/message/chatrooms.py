import tkinter as tk

class ChatroomsWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chatrooms")
        
        # Set the size and position of the window
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create labels for different categories
        self.label_us_states = tk.Label(self.root, text="US States", font=('Helvetica', 14, 'bold'))
        self.label_us_states.pack(pady=5, anchor='w')

        self.label_northeast = tk.Label(self.root, text="Northeast", font=('Helvetica', 12, 'bold'))
        self.label_northeast.pack(pady=5, anchor='w')

        self.label_midwest = tk.Label(self.root, text="Midwest", font=('Helvetica', 12, 'bold'))
        self.label_midwest.pack(pady=5, anchor='w')

        self.label_south = tk.Label(self.root, text="South", font=('Helvetica', 12, 'bold'))
        self.label_south.pack(pady=5, anchor='w')

        self.label_west = tk.Label(self.root, text="West", font=('Helvetica', 12, 'bold'))
        self.label_west.pack(pady=5, anchor='w')

        # Create buttons for each state under respective categories
        self.create_state_buttons(self.label_northeast, ['Connecticut', 'Maine', 'Massachusetts', 'New Hampshire', 'Rhode Island', 'Vermont'])
        self.create_state_buttons(self.label_midwest, ['Illinois', 'Indiana', 'Iowa', 'Kansas', 'Michigan', 'Minnesota', 'Missouri', 'Nebraska', 'North Dakota', 'Ohio', 'South Dakota', 'Wisconsin'])
        self.create_state_buttons(self.label_south, ['Alabama', 'Arkansas', 'Delaware', 'Florida', 'Georgia', 'Kentucky', 'Louisiana', 'Maryland', 'Mississippi', 'North Carolina', 'Oklahoma', 'South Carolina', 'Tennessee', 'Texas', 'Virginia', 'West Virginia'])
        self.create_state_buttons(self.label_west, ['Alaska', 'Arizona', 'California', 'Colorado', 'Hawaii', 'Idaho', 'Montana', 'Nevada', 'New Mexico', 'Oregon', 'Utah', 'Washington', 'Wyoming'])

        self.root.mainloop()

    def create_state_buttons(self, parent, states):
        for state in states:
            button = tk.Button(parent, text=state, font=('Helvetica', 10), width=15)
            button.pack(side='left', padx=5, pady=2)

if __name__ == "__main__":
    ChatroomsWindow()
