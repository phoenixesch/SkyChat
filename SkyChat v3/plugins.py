import tkinter as tk
from tkinter import font, filedialog
import os

class PluginWindow:
    PLUGIN_FOLDER = "plugins"

    def __init__(self, master):
        self.master = master
        self.master.title("Plugin Window")

        # Define a bold font with size 20
        title_font = font.Font(family="Helvetica", size=20, weight="bold")

        # Create a label with the title
        self.title_label = tk.Label(self.master, text="Plugin Window", font=title_font)
        self.title_label.pack(pady=10)

        # Create an "Upload" button
        self.upload_button = tk.Button(self.master, text="Upload", command=self.upload_plugin)
        self.upload_button.pack(pady=5)

        # Create an "Exit" button
        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.destroy)
        self.exit_button.pack(pady=5)

    def upload_plugin(self):
        # Open file dialog to select a Python (.py) file
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if file_path:
            # Check if the plugins folder exists, if not, create it
            if not os.path.exists(self.PLUGIN_FOLDER):
                os.makedirs(self.PLUGIN_FOLDER)

            # Get the file name
            file_name = os.path.basename(file_path)

            # Copy the file to the plugins folder
            destination_path = os.path.join(self.PLUGIN_FOLDER, file_name)

            # Open the source file for reading
            with open(file_path, 'r') as src_file:
                # Open the destination file for writing
                with open(destination_path, 'w') as dest_file:
                    # Copy the contents of the source file to the destination file
                    dest_file.write(src_file.read())

            tk.messagebox.showinfo("Plugin Installed", f"Plugin '{file_name}' installed successfully!")
        else:
            tk.messagebox.showinfo("Info", "No file selected.")

def main():
    root = tk.Tk()
    app = PluginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
