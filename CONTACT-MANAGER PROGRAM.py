import tkinter as tk
from tkinter import messagebox, ttk

FILE = "contacts.txt"

def load_contacts():
    contacts = []
    try:
        with open(FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    contacts.append(parts)
    except FileNotFoundError:
        pass
    return contacts

def refresh_table():
    table.delete(*table.get_children())
    for i, c in enumerate(load_contacts()):
        table.insert("", "end", values=(i + 1, c[0], c[1], c[2]))

def on_row_click(event):
    selected = table.selection()
    if not selected:
        return
    values = table.item(selected[0])["values"]
    entry_name.delete(0, tk.END)
    entry_number.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_name.insert(0, values[1])
    entry_number.insert(0, values[2])
    entry_address.insert(0, values[3])

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_number.delete(0, tk.END)
    entry_address.delete(0, tk.END)

def add_contact():
    name    = entry_name.get().strip()
    number  = entry_number.get().strip()
    address = entry_address.get().strip()

    if not name or not number or not address:
        messagebox.showwarning("Empty Fields", "Please fill in all fields.")
        return
    if not number.replace("+", "").replace("-", "").isdigit():
        messagebox.showwarning("Invalid Number", "Number must be digits only.")
        return

    contacts = load_contacts()
    contacts.append([name, number, address])
    save_contacts(contacts)
    refresh_table()
    clear_fields()
    messagebox.showinfo("Success", f'"{name}" added!')


def update_contact():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Click a contact row first.")
        return

    name    = entry_name.get().strip()
    number  = entry_number.get().strip()
    address = entry_address.get().strip()

    if not name or not number or not address:
        messagebox.showwarning("Empty Fields", "Please fill in all fields.")
        return

    contacts = load_contacts()
    index = table.index(selected[0])
    contacts[index] = [name, number, address]
    save_contacts(contacts)
    refresh_table()
    clear_fields()
    messagebox.showinfo("Success", f'"{name}" updated!')


def delete_contact():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Click a contact row first.")
        return

    name = table.item(selected[0])["values"][1]
    if messagebox.askyesno("Confirm", f'Delete "{name}"?'):
        contacts = load_contacts()
        contacts.pop(table.index(selected[0]))
        save_contacts(contacts)
        refresh_table()
        clear_fields()


def search_contact(*args):
    query = search_var.get().strip().lower()
    if not query:
        refresh_table()
        return
    table.delete(*table.get_children())
    for i, c in enumerate(load_contacts()):
        if query in c[0].lower() or query in c[1] or query in c[2].lower():
            table.insert("", "end", values=(i + 1, c[0], c[1], c[2]))

# GUI (TKinter)
window = tk.Tk()
window.title("Contact Manager")
window.geometry("750x520")
window.resizable(False, False)
window.configure(bg="#f0f4f8")

title_frame = tk.Frame(window, bg="#1a1a2e", height=70)
title_frame.pack(fill="x")
title_frame.pack_propagate(False) 

tk.Label(
    title_frame,
    text="📞  Contact Management System",
    font=("Century Gothic", 22, "bold"), 
    bg="#52b6eb",                
    fg="#ffffff",                    
    anchor="center"                   
).pack(expand=True, fill="both")     

main = tk.Frame(window, bg="#52b6eb")
main.pack(fill="both", expand=True, padx=15, pady=25)

form = tk.LabelFrame(main, text="Contact Details", padx=10, pady=10)
form.pack(side="left", fill="y", padx=(0, 10))

tk.Label(form, text="Name:").grid(row=0, column=0, sticky="w", pady=4)
entry_name = tk.Entry(form, width=25)
entry_name.grid(row=0, column=1, pady=4)

tk.Label(form, text="Number:").grid(row=1, column=0, sticky="w", pady=4)
entry_number = tk.Entry(form, width=25)
entry_number.grid(row=1, column=1, pady=4)

tk.Label(form, text="Address:").grid(row=2, column=0, sticky="w", pady=4)
entry_address = tk.Entry(form, width=25)
entry_address.grid(row=2, column=1, pady=4)

tk.Label(form, text="Search:").grid(row=3, column=0, sticky="w", pady=4)
entry_search = tk.Entry(form, width=25)
entry_search.grid(row=3, column=1, pady=4)

tk.Button(form, text="Add",    width=20, bg="#27ae60", fg="white", command=add_contact   ).grid(row=4, columnspan=2, pady=3)
tk.Button(form, text="Update", width=20, bg="#2980b9", fg="white", command=update_contact).grid(row=5, columnspan=2, pady=3)
tk.Button(form, text="Delete", width=20, bg="#e74c3c", fg="white", command=delete_contact).grid(row=6, columnspan=2, pady=3)
tk.Button(form, text="Search", width=20, bg="#8e44ad", fg="white", command=search_contact).grid(row=7, columnspan=2, pady=3)
tk.Button(form, text="Clear",  width=20, bg="#b37700", fg="white", command=clear_form   ).grid(row=8, columnspan=2, pady=3)

right = tk.LabelFrame(main, text="Contact Records", padx=5, pady=5)
right.pack(side="left", fill="both", expand=True)

table = ttk.Treeview(right, columns=("#", "Name", "Number", "Address"), show="headings")
table.heading("#",       text="#")
table.heading("Name",    text="Name")
table.heading("Number",  text="Number")
table.heading("Address", text="Address")
table.column("#",       width=30,  anchor="center")
table.column("Name",    width=130)
table.column("Number",  width=110)
table.column("Address", width=150)
table.pack(fill="both", expand=True)
table.bind("<<TreeviewSelect>>", on_row_click)

refresh_table()

window.mainloop()



