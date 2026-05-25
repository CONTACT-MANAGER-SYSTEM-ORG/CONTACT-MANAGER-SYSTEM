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


def save_contacts(contacts):
    with open(FILE, "w") as f:
        for c in contacts:
            f.write(c[0] + "|" + c[1] + "|" + c[2] + "\n")



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
    search_text = search_variable.get().strip().lower()
    if not search_text:
        refresh_table()
        return
    table.delete(*table.get_children())
    for i, c in enumerate(load_contacts()):
        if search_text in c[0].lower() or search_text in c[1] or search_text in c[2].lower():
            table.insert("", "end", values=(i + 1, c[0], c[1], c[2]))



window = tk.Tk()
window.title("Contact Manager")
window.geometry("1000x600")
window.resizable(True, True)
window.configure(bg="#52b6eb")


tk.Label(window, text="📞 Contact Management System",
         font=("Century Gothic", 20, "bold"),
         bg="#52b6eb", fg="white").pack(pady=10)


search_bar = tk.Frame(window, bg="#1a6fa8", pady=6)
search_bar.pack(fill="x")

tk.Label(search_bar, text="🔍 Search:",
         font=("Century Gothic", 14, "bold"),
         bg="#1a6fa8", fg="white").pack(side="left", padx=(12, 6))

search_variable = tk.StringVar()
search_variable.trace("w", search_contact)  

tk.Entry(search_bar, textvariable=search_variable,
         width=38, font=("Century Gothic", 11),
         bg="white", fg="#1a1a2e",
         relief="solid", bd=3).pack(side="left", ipady=5)


main = tk.Frame(window, bg="#52b6eb")
main.pack(fill="both", expand=True, padx=15, pady=10)


Entry_style = dict(width=24, font=("Century Gothic", 10, "bold"),
         bg="white", fg="#000000", relief="solid", bd=2)
Label_stlye = dict(font=("Century Gothic", 10, "bold"), bg="#52b6eb", fg="white")
Button_style = dict(width=20, font=("Century Gothic", 10, "bold"),
         fg="white", relief="sunken", cursor="hand1", pady=4)


form = tk.LabelFrame(main, text="Contact Details",
                     font=("Century Gothic", 10, "bold"),
                     bg="#52b6eb", fg="white", padx=10, pady=10)
form.pack(side="left", fill="y", padx=(0, 10))

tk.Label(form, text="Name:",    **Label_stlye).grid(row=0, column=0, sticky="w", pady=5)
entry_name = tk.Entry(form, **Entry_style)
entry_name.grid(row=0, column=1, pady=5, ipady=5)

tk.Label(form, text="Number:", **Label_stlye).grid(row=1, column=0, sticky="w", pady=5)
entry_number = tk.Entry(form, **Entry_style)
entry_number.grid(row=1, column=1, pady=5, ipady=5)

tk.Label(form, text="Address:", **Label_stlye).grid(row=2, column=0, sticky="w", pady=5)
entry_address = tk.Entry(form, **Entry_style)
entry_address.grid(row=2, column=1, pady=5, ipady=5)

tk.Button(form, text="Add",    bg="#27ae60", command=add_contact,    **Button_style).grid(row=3, columnspan=2, pady=3)
tk.Button(form, text="Update", bg="#2980b9", command=update_contact, **Button_style).grid(row=4, columnspan=2, pady=3)
tk.Button(form, text="Delete", bg="#e74c3c", command=delete_contact, **Button_style).grid(row=5, columnspan=2, pady=3)


contact_list_table = tk.LabelFrame(main, text="Contact Records",
                      font=("Century Gothic", 10, "bold"),
                      bg="#52b6eb", fg="white", padx=5, pady=5)
contact_list_table.pack(side="left", fill="both", expand=True)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", font=("Century Gothic", 10), rowheight=26,
                background="#f7fbff", fieldbackground="#f7fbff", foreground="#1a1a2e")
style.configure("Treeview.Heading", font=("Century Gothic", 10, "bold"),
                background="#1a6fa8", foreground="white")
style.map("Treeview", background=[("selected", "#2980b9")])

contact_columns = ["#", "Name", "Number", "Address"]
table = ttk.Treeview(contact_list_table, columns=contact_columns, show="headings")

for column in contact_columns:
    table.heading(column, text=column, anchor="center")
    table.column(column, width=100, anchor="center")

scrollbar = ttk.Scrollbar(contact_list_table, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)
table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
table.bind("<<TreeviewSelect>>", on_row_click)

refresh_table()

window.mainloop()
