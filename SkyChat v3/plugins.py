import tkinter as tk
from tkinter import font, filedialog
import os
class PluginWindow:
    PLUGIN_FOLDER = "plugins"
    def __init__(self, master):
        self.master = master
        self.master.title("Plugin Window")
        title_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.title_label = tk.Label(self.master, text="Plugin Window", font=title_font)
        self.title_label.pack(pady=10)
        self.upload_button = tk.Button(self.master, text="Upload", command=self.upload_plugin)
        self.upload_button.pack(pady=5)
        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.destroy)
        self.exit_button.pack(pady=5)
    def upload_plugin(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if file_path:
            if not os.path.exists(self.PLUGIN_FOLDER):
                os.makedirs(self.PLUGIN_FOLDER)
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(self.PLUGIN_FOLDER, file_name)
            with open(file_path, 'r') as src_file:
                with open(destination_path, 'w') as dest_file:
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
