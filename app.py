import tkinter as tk
from tkinter import ttk, filedialog
import os
from batchFile import startBatch


task_list = os.path.join(os.getcwd(), 'task_list.txt')
task = 'autobot.py'
class TaskInputApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Drone Image Processing")

        # Task Name
        self.task_label = tk.Label(master, text="Task Name:")
        self.task_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.task_entry = tk.Entry(master, width=40)
        self.task_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

        # Source Folder
        self.source_label = tk.Label(master, text="Source Folder:")
        self.source_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.source_var = tk.StringVar()
        self.source_label_display = tk.Label(master, text="", width=40, anchor="w", relief="solid")
        self.source_label_display.grid(row=1, column=1, columnspan=2, padx=10, pady=5)
        self.source_button = tk.Button(master, text="Browse", command=self.browse_source)
        self.source_button.grid(row=1, column=3, padx=5, pady=5)

        # Destination Folder
        self.dest_label = tk.Label(master, text="Destination Folder:")
        self.dest_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.dest_var = tk.StringVar()
        self.dest_label_display = tk.Label(master, text="", width=40, anchor="w", relief="solid")
        self.dest_label_display.grid(row=2, column=1, columnspan=2, padx=10, pady=5)
        self.dest_button = tk.Button(master, text="Browse", command=self.browse_dest)
        self.dest_button.grid(row=2, column=3, padx=5, pady=5)

        # Time Schedule
        self.time_label = tk.Label(master, text="Time Schedule:")
        self.time_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        # Hour Dropdown
        self.hour_var = tk.StringVar(value="00")
        self.hour_dropdown = ttk.Combobox(master, textvariable=self.hour_var, values=[str(i).zfill(2) for i in range(24)], width=2)
        self.hour_dropdown.grid(row=3, column=1, padx=3, pady=3)

        # Minute Dropdown
        self.minute_var = tk.StringVar(value="00")
        self.minute_dropdown = ttk.Combobox(master, textvariable=self.minute_var, values=[str(i).zfill(2) for i in range(60)], width=2)
        self.minute_dropdown.grid(row=3, column=2, padx=3, pady=3)

        # Second Dropdown
        self.second_var = tk.StringVar(value="00")
        self.second_dropdown = ttk.Combobox(master, textvariable=self.second_var, values=[str(i).zfill(2) for i in range(60)], width=2)
        self.second_dropdown.grid(row=3, column=3, padx=3, pady=3)

        # Submit Button
        self.submit_button = tk.Button(master, text="Submit", command=self.submit)
        self.submit_button.grid(row=4, column=1, columnspan=2, pady=10)

        # Frame for Displaying File Names
        self.file_frame = tk.Frame(master, bg="white", width=400, height=200)
        self.file_frame.grid(row=0, column=4, rowspan=5, padx=10, pady=10)

        # Label for File List
        self.file_list_label = tk.Label(self.file_frame, text="File List:", bg="white")
        self.file_list_label.pack()

        # Listbox for Displaying File Names
        self.file_listbox = tk.Listbox(self.file_frame, selectmode=tk.SINGLE)
        self.file_listbox.pack(expand=True, fill="both")

        # Delete Button for Removing Selected File
        self.delete_button = tk.Button(self.file_frame, text="Delete", command=self.delete_file)
        self.delete_button.pack(pady=5)

        self.populate_file_list()
        startBatch(task_list)

    def browse_source(self):
        source_folder = filedialog.askdirectory()
        self.source_var.set(source_folder)
        self.source_label_display.config(text=source_folder)

    def browse_dest(self):
        dest_folder = filedialog.askdirectory()
        self.dest_var.set(dest_folder)
        self.dest_label_display.config(text=dest_folder)

    def submit(self):
        task_name = self.task_entry.get()
        source_folder = self.source_var.get()
        dest_folder = self.dest_var.get()
        time_schedule = f"{self.hour_var.get()}:{self.minute_var.get()}:{self.second_var.get()}"

        with open(task_list, "a") as file:
            file.write(f"{task_name} | {source_folder} | {dest_folder} | {time_schedule}\n")

        self.task_entry.delete(0, tk.END)
        self.source_var.set("")
        self.source_label_display.config(text="")
        self.dest_var.set("")
        self.dest_label_display.config(text="")
        self.hour_dropdown.set("00")
        self.minute_dropdown.set("00")
        self.second_dropdown.set("00")

        self.populate_file_list()

    def populate_file_list(self):
        self.file_listbox.delete(0, tk.END)  # Clear existing items
        try:
            with open(task_list, "r") as file:
                filenames = file.readlines()
                for filename in filenames:
                    self.file_listbox.insert(tk.END, filename.strip())
        except FileNotFoundError:
            print("File not found. Creating a new task_list.txt.")

    def delete_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_filename = self.file_listbox.get(selected_index)
            self.file_listbox.delete(selected_index)

            # Update task_list.txt
            with open(task_list, "r") as file:
                filenames = file.readlines()

            with open(task_list, "w") as file:
                for filename in filenames:
                    if filename.strip() != selected_filename:
                        file.write(filename)

def app():
    root = tk.Tk()
    TaskInputApp(root)
    root.mainloop()

if __name__ == "__main__":
    app()