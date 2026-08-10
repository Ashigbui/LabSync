import tkinter as tk


equipment_list = [
    "Microscope — Available",
    "Centrifuge — Available",
    "Test tubes — In use"
]


def show_equipment():
    equipment_box.delete(0, tk.END)

    for equipment in equipment_list:
        equipment_box.insert(tk.END, equipment)


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
    width=50,
    height=10,
    font=("Arial", 12)
)
equipment_box.pack(pady=20)

window.mainloop()
