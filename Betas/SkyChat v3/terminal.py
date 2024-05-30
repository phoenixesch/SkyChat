import tkinter as tk
from tkinter import font

class VirtualTerminal:
    def __init__(self, master):
        self.master = master
        self.master.title("Virtual Terminal")

        # Configure monospaced font for input and output text
        self.font = font.Font(family="Courier New", size=10)

        # Create and pack the input entry
        self.input_entry = tk.Entry(self.master, font=self.font)
        self.input_entry.pack(fill=tk.BOTH, expand=True)
        self.input_entry.focus()  # Set focus to input entry

        # Create and pack the output text
        self.output_text = tk.Text(self.master, height=20, width=80, font=self.font)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Bind Enter key to process command
        self.input_entry.bind("<Return>", self.process_command)

        # Display command prompt symbol
        self.output_text.insert(tk.END, ">> ")

    def process_command(self, event):
        command = self.input_entry.get()
        self.input_entry.delete(0, tk.END)  # Clear input entry
        self.output_text.insert(tk.END, f"\n{command}\n")
        self.output_text.insert(tk.END, ">> ")  # Display command prompt symbol for next input

        if command.lower() == "help":
            self.output_text.insert(tk.END, "Available commands:\n")
            self.output_text.insert(tk.END, "1. help - Display available commands\n")
            self.output_text.insert(tk.END, "2. exit - Exit the virtual terminal\n")
        elif command.lower() == "exit":
            self.master.destroy()  # Close the virtual terminal window
        else:
            self.output_text.insert(tk.END, "Invalid command. Type 'help' for available commands.\n")

def main():
    root = tk.Tk()
    app = VirtualTerminal(root)
    root.mainloop()

if __name__ == "__main__":
    main()
