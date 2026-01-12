import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import csv
import os
import shutil
import datetime

# CONFIGURATION
CSV_FILE = 'links.csv'
FILES_DIR = 'files'

# Ensure files directory exists
if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)

# Ensure CSV exists with header
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        f.write("Title,Url,Type\n")

def append_to_csv(title, url, link_type):
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([title, url, link_type])

def add_web_link():
    title = simpledialog.askstring("Input", "Enter Link Title:")
    if not title: return
    
    url = simpledialog.askstring("Input", "Enter URL (e.g., https://google.com):")
    if not url: return

    append_to_csv(title, url, "web")
    messagebox.showinfo("Success", f"Added web link: {title}")

def add_local_file():
    # 1. Ask for the file
    filepath = filedialog.askopenfilename(title="Select a file to upload")
    if not filepath: return

    # 2. Ask for a title
    title = simpledialog.askstring("Input", "Enter File Title:")
    if not title: 
        title = os.path.basename(filepath) # Default to filename

    # 3. Copy file to the 'files' folder
    filename = os.path.basename(filepath)
    destination = os.path.join(FILES_DIR, filename)
    
    # Handle duplicate filenames
    if os.path.exists(destination):
        base, ext = os.path.splitext(filename)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{base}_{timestamp}{ext}"
        destination = os.path.join(FILES_DIR, filename)

    shutil.copy2(filepath, destination)

    # 4. Update CSV with relative path
    # We use forward slashes for web compatibility
    relative_path = f"{FILES_DIR}/{filename}"
    append_to_csv(title, relative_path, "file")
    
    messagebox.showinfo("Success", f"File copied & added: {title}")

def main():
    root = tk.Tk()
    root.title("Website Manager")
    root.geometry("300x200")

    label = tk.Label(root, text="Manage Your Links", font=("Arial", 14))
    label.pack(pady=20)

    btn_web = tk.Button(root, text="Add Web Link 🔗", command=add_web_link, width=20, bg="#e7f3fe")
    btn_web.pack(pady=5)

    btn_file = tk.Button(root, text="Add Local File 📂", command=add_local_file, width=20, bg="#e6ffed")
    btn_file.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()