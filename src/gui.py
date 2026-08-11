import json
import tkinter as tk
from pathlib import Path


# Finds equipment.json regardless of where you run the program from
PROJECT_FOLDER = Path(__file__).resolve().parent.parent
EQUIPMENT_FILE = PROJECT_FOLDER / "data" / "equipment.json"


def show_equipment():
    equipment_box.delete(0, tk.END)

    try:
        with open(EQUIPMENT_FILE, "r", encoding="utf-8") as file:
            equipment_list = json.load(file)

        if not equipment_list:
            equipment_box.insert(tk.END, "No equipment has been added.")
            return

        for equipment in equipment_list:
            equipment_id = equipment.get("id", "")
            name = equipment.get("name", "")
            status = equipment.get("status", "")

            equipment_box.insert(
                tk.END,
                f"{equipment_id} — {name} — {status}"
            )

    except FileNotFoundError:
        equipment_box.insert(tk.END, "equipment.json was not found.")

    except json.JSONDecodeError:
        equipment_box.insert(tk.END, "equipment.json contains invalid JSON.")


window = tk.Tk()
window.title("LabSync")
window.geometry("700x450")

heading = tk.Label(
    window,
    text="LabSync Laboratory Management System",
    font=("Arial", 20, "bold")
)
heading.pack(pady=30)

equipment_button = tk.Button(
    window,
    text="View Equipment",
    command=show_equipment
)
equipment_button.pack(pady=10)

equipment_box = tk.Listbox(
    window,
    width=60,
    height=10,
    font=("Arial", 12)
)
equipment_box.pack(pady=20)

window.mainloop()
