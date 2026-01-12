import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import csv
import os
import shutil
import datetime
import subprocess  # <--- Added to run git commands

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
    filepath = filedialog.askopenfilename(title="Select a file to upload")
    if not filepath: return

    title = simpledialog.askstring("Input", "Enter File Title:")
    if not title: 
        title = os.path.basename(filepath)

    filename = os.path.basename(filepath)
    destination = os.path.join(FILES_DIR, filename)
    
    # Handle duplicate filenames
    if os.path.exists(destination):
        base, ext = os.path.splitext(filename)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{base}_{timestamp}{ext}"
        destination = os.path.join(FILES_DIR, filename)

    shutil.copy2(filepath, destination)

    # Use forward slashes for web compatibility
    relative_path = f"{FILES_DIR}/{filename}"
    append_to_csv(title, relative_path, "file")
    
    messagebox.showinfo("Success", f"File copied & added: {title}")

def publish_changes():
    """Runs the git commands to push changes to GitHub"""
    confirm = messagebox.askyesno("Publish", "This will sync changes to GitHub.\nAre you sure?")
    if not confirm: return

    try:
        # 1. Git Add
        subprocess.run(["git", "add", "."], check=True)
        
        # 2. Git Commit
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        subprocess.run(["git", "commit", "-m", f"Update links: {timestamp}"], check=True)
        
        # 3. Git Push
        subprocess.run(["git", "push"], check=True)
        
        messagebox.showinfo("Published", "Success! Changes are live on GitHub in ~2 mins.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Git Error:\n{e}")
    except FileNotFoundError:
        messagebox.showerror("Error", "Git is not installed or not found in PATH.")

def main():
    root = tk.Tk()
    root.title("Website Manager")
    root.geometry("350x300")

    label = tk.Label(root, text="Manage Your Links", font=("Segoe UI", 14, "bold"))
    label.pack(pady=20)

    # Buttons
    tk.Button(root, text="Add Web Link 🔗", command=add_web_link, width=25, bg="#e7f3fe").pack(pady=5)
    tk.Button(root, text="Add Local File 📂", command=add_local_file, width=25, bg="#e6ffed").pack(pady=5)
    
    # Separator
    tk.Frame(root, height=2, bd=1, relief="sunken").pack(fill="x", padx=20, pady=15)

    # Publish Button (Red/Important)
    tk.Button(root, text="☁️ Publish to GitHub", command=publish_changes, width=25, bg="#ffe6e6", fg="#d63384").pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()