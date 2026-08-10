import tkinter as tk


def show_equipment():
    message_label.config(text="Equipment section selected")


window = tk.Tk()
window.title("LabSync")
window.geometry("700x450")

heading = tk.Label(
    window,
    text="LabSync Laboratory Management System",
    font=("Arial", 20, "bold")
)
heading.pack(pady=30)

description = tk.Label(
    window,
    text="Manage laboratory equipment, bookings, and returns."
)
description.pack(pady=10)

equipment_button = tk.Button(
    window,
    text="View Equipment",
    command=show_equipment
)
equipment_button.pack(pady=20)

message_label = tk.Label(
    window,
    text=""
)
message_label.pack()

window.mainloop()
