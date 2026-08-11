import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


PROJECT_FOLDER = Path(__file__).resolve().parent.parent
EQUIPMENT_FILE = PROJECT_FOLDER / "data" / "equipment.json"


def read_equipment():
    try:
        with open(EQUIPMENT_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def show_equipment():
    equipment_box.delete(0, tk.END)

    equipment_list = read_equipment()

    if not equipment_list:
        equipment_box.insert(tk.END, "No equipment has been added.")
        return

    for equipment in equipment_list:
        equipment_box.insert(
            tk.END,
            f'{equipment.get("id", "")} — '
            f'{equipment.get("name", "")} — '
            f'{equipment.get("status", "")}'
        )


def add_equipment():
    equipment_id = id_entry.get().strip()
    equipment_name = name_entry.get().strip()

    if not equipment_id or not equipment_name:
        messagebox.showerror("Error", "Please complete both fields.")
        return

    equipment_list = read_equipment()

    for equipment in equipment_list:
        if equipment.get("id", "").lower() == equipment_id.lower():
            messagebox.showerror("Error", "That equipment ID already exists.")
            return

    equipment_list.append({
        "id": equipment_id,
        "name": equipment_name,
        "status": "Available"
    })

    with open(EQUIPMENT_FILE, "w", encoding="utf-8") as file:
        json.dump(equipment_list, file, indent=4)

    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)

    show_equipment()
    messagebox.showinfo("Success", "Equipment added successfully.")


window = tk.Tk()
window.title("LabSync")
window.geometry("700x600")

heading = tk.Label(
    window,
    text="LabSync Laboratory Management System",
    font=("Arial", 20, "bold")
)
heading.pack(pady=20)

id_label = tk.Label(window, text="Equipment ID")
id_label.pack()

id_entry = tk.Entry(window, width=35)
id_entry.pack(pady=5)

name_label = tk.Label(window, text="Equipment name")
name_label.pack()

name_entry = tk.Entry(window, width=35)
name_entry.pack(pady=5)

add_button = tk.Button(
    window,
    text="Add Equipment",
    command=add_equipment
)
add_button.pack(pady=10)

view_button = tk.Button(
    window,
    text="View Equipment",
    command=show_equipment
)
view_button.pack(pady=5)

equipment_box = tk.Listbox(
    window,
    width=60,
    height=10,
    font=("Arial", 12)
)
equipment_box.pack(pady=15)

window.mainloop()
