import tkinter as tk


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
    text="Manage laboratory equipment, bookings and returns."
)
description.pack(pady=10)

window.mainloop()
