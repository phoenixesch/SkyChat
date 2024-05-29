import tkinter as tk

class Terminal:
    def __init__(self, master):
        self.master = master
        self.master.title("Terminal")

        self.output_text = tk.Text(self.master, wrap="word", state="disabled")
        self.output_text.pack(expand=True, fill="both")

        self.input_entry = tk.Entry(self.master)
        self.input_entry.pack(side="bottom", fill="x")
        self.input_entry.bind("<Return>", self.handle_input)

        self.output_text.tag_configure("prompt", foreground="blue")

        self.print_prompt()

    def handle_input(self, event):
        command = self.input_entry.get()
        self.print_command(command)
        self.input_entry.delete(0, "end")
        self.execute_command(command)

    def print_prompt(self):
        self.output_text.configure(state="normal")
        self.output_text.insert("end", ">> ", "prompt")
        self.output_text.configure(state="disabled")

    def print_command(self, command):
        self.output_text.configure(state="normal")
        self.output_text.insert("end", f"{command}\n")
        self.output_text.configure(state="disabled")

    def execute_command(self, command):
        if command.lower() == "help":
            self.print_output("Available commands:\n - help: Show available commands\n - exit: Close the terminal")
        elif command.lower() == "exit":
            self.master.destroy()
        else:
            self.print_output(f"Command '{command}' not recognized")

    def print_output(self, output):
        self.output_text.configure(state="normal")
        self.output_text.insert("end", f"{output}\n")
        self.output_text.see("end")
        self.output_text.configure(state="disabled")
        self.print_prompt()

def main():
    root = tk.Tk()
    app = Terminal(root)
    root.mainloop()

if __name__ == "__main__":
    main()
