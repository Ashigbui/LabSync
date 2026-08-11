import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from equipment import Equipment


PROJECT_FOLDER = Path(__file__).resolve().parent.parent
EQUIPMENT_FILE = PROJECT_FOLDER / "data" / "equipment.json"


def read_equipment():
    try:
        with open(EQUIPMENT_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_equipment(equipment_list):
    with open(EQUIPMENT_FILE, "w", encoding="utf-8") as file:
        json.dump(equipment_list, file, indent=4)


def show_equipment():
    equipment_box.delete(0, tk.END)

    equipment_list = read_equipment()

    if not equipment_list:
        equipment_box.insert(tk.END, "No equipment has been added.")
        return

    for equipment in equipment_list:
        # Supports both the old "id" and new "equipment_id" format
        equipment_id = equipment.get(
            "equipment_id",
            equipment.get("id", "")
        )

        name = equipment.get("name", "")
        category = equipment.get("category", "Not specified")
        quantity = equipment.get("quantity", 1)
        status = equipment.get("status", "available")

        equipment_box.insert(
            tk.END,
            f"{equipment_id} — {name} — {category} — "
            f"Quantity: {quantity} — {status}"
        )


def add_equipment():
    equipment_id = id_entry.get().strip()
    name = name_entry.get().strip()
    category = category_entry.get().strip()
    quantity_text = quantity_entry.get().strip()

    if not equipment_id or not name or not category or not quantity_text:
        messagebox.showerror(
            "Error",
            "Please complete every field."
        )
        return

    try:
        quantity = int(quantity_text)

        if quantity <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Error",
            "Quantity must be a positive whole number."
        )
        return

    equipment_list = read_equipment()

    for saved_equipment in equipment_list:
        saved_id = saved_equipment.get(
            "equipment_id",
            saved_equipment.get("id", "")
        )

        if saved_id.lower() == equipment_id.lower():
            messagebox.showerror(
                "Error",
                "That equipment ID already exists."
            )
            return

    new_equipment = Equipment(
        equipment_id=equipment_id,
        name=name,
        category=category,
        laboratory="Main Laboratory",
        quantity=quantity,
        available_quantity=quantity,
        status="available",
        safety_instructions="Follow laboratory safety rules."
    )

    equipment_list.append(new_equipment.display_details())
    save_equipment(equipment_list)

    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)

    show_equipment()

    messagebox.showinfo(
        "Success",
        "Equipment added successfully."
    )


window = tk.Tk()
window.title("LabSync")
window.geometry("850x650")

heading = tk.Label(
    window,
    text="LabSync Laboratory Management System",
    font=("Arial", 20, "bold")
)
heading.pack(pady=20)

tk.Label(window, text="Equipment ID").pack()
id_entry = tk.Entry(window, width=35)
id_entry.pack(pady=5)

tk.Label(window, text="Equipment name").pack()
name_entry = tk.Entry(window, width=35)
name_entry.pack(pady=5)

tk.Label(window, text="Category").pack()
category_entry = tk.Entry(window, width=35)
category_entry.pack(pady=5)

tk.Label(window, text="Quantity").pack()
quantity_entry = tk.Entry(window, width=35)
quantity_entry.pack(pady=5)

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
    width=85,
    height=10,
    font=("Arial", 12)
)
equipment_box.pack(pady=15)

window.mainloop()
     
