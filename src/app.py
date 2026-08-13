import json
from datetime import date
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

from bookings import Booking
from equipment import Equipment


PROJECT_FOLDER = Path(__file__).resolve().parent.parent
EQUIPMENT_FILE = PROJECT_FOLDER / "data" / "equipment.json"
BOOKINGS_FILE = PROJECT_FOLDER / "data" / "bookings.json"

app = Flask(__name__, template_folder=str(PROJECT_FOLDER / "templates"), static_folder=str(PROJECT_FOLDER / "static"))


def read_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_json(file_path, data):
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def read_equipment():
    return read_json(EQUIPMENT_FILE)


def save_equipment(equipment_list):
    save_json(EQUIPMENT_FILE, equipment_list)


def read_bookings():
    return read_json(BOOKINGS_FILE)


def save_bookings(booking_list):
    save_json(BOOKINGS_FILE, booking_list)


@app.route("/")
def home():
    return render_template("index.html", equipment_list=read_equipment(), booking_list=read_bookings())


@app.route("/add", methods=["POST"])
def add_equipment():
    equipment_id = request.form.get("equipment_id", "").strip()
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    quantity_text = request.form.get("quantity", "").strip()

    if not equipment_id or not name or not category or not quantity_text:
        return redirect(url_for("home", message="Please complete every equipment field."))

    try:
        quantity = int(quantity_text)

        if quantity <= 0:
            raise ValueError
    except ValueError:
        return redirect(url_for("home", message="Quantity must be a positive whole number."))

    equipment_list = read_equipment()

    for saved_equipment in equipment_list:
        saved_id = saved_equipment.get("equipment_id", saved_equipment.get("id", ""))

        if saved_id.lower() == equipment_id.lower():
            return redirect(url_for("home", message="That equipment ID already exists."))

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

    return redirect(url_for("home", message="Equipment added successfully."))


@app.route("/delete/<equipment_id>", methods=["POST"])
def delete_equipment(equipment_id):
    equipment_list = read_equipment()
    booking_list = read_bookings()

    for booking in booking_list:
        if booking.get("equipment", "").lower() == equipment_id.lower() and booking.get("status") in {"Active", "Overdue"}:
            return redirect(url_for("home", message="This equipment has an active booking and cannot be deleted."))

    updated_list = [
        equipment
        for equipment in equipment_list
        if equipment.get("equipment_id", equipment.get("id", "")).lower() != equipment_id.lower()
    ]

    save_equipment(updated_list)
    return redirect(url_for("home", message="Equipment deleted successfully."))


@app.route("/book", methods=["POST"])
def book_equipment():
    student = request.form.get("student", "").strip()
    equipment_id = request.form.get("booking_equipment", "").strip()
    quantity_text = request.form.get("booking_quantity", "").strip()
    return_date = request.form.get("return_date", "").strip()
    purpose = request.form.get("purpose", "").strip()

    if not student or not equipment_id or not quantity_text or not return_date or not purpose:
        return redirect(url_for("home", message="Please complete every booking field."))

    try:
        quantity = int(quantity_text)

        if quantity <= 0:
            raise ValueError
    except ValueError:
        return redirect(url_for("home", message="Booking quantity must be a positive whole number."))

    try:
        chosen_return_date = date.fromisoformat(return_date)

        if chosen_return_date < date.today():
            return redirect(url_for("home", message="The return date cannot be in the past."))
    except ValueError:
        return redirect(url_for("home", message="Please enter a valid return date."))

    equipment_list = read_equipment()
    selected_equipment = None

    for equipment in equipment_list:
        saved_id = equipment.get("equipment_id", equipment.get("id", ""))

        if saved_id.lower() == equipment_id.lower():
            selected_equipment = equipment
            break

    if selected_equipment is None:
        return redirect(url_for("home", message="The selected equipment was not found."))

    available_quantity = selected_equipment.get("available_quantity", selected_equipment.get("quantity", 1))

    if quantity > available_quantity:
        return redirect(url_for("home", message="There is not enough equipment available."))

    booking_list = read_bookings()
    booking_id = f"BK{len(booking_list) + 1:03d}"

    existing_ids = {booking.get("booking_id", "") for booking in booking_list}

    while booking_id in existing_ids:
        booking_id = f"BK{int(booking_id[2:]) + 1:03d}"

    new_booking = Booking(
        booking_id=booking_id,
        student=student,
        equipment=equipment_id,
        booking_date=date.today(),
        start_time=date.today(),
        return_time=chosen_return_date,
        purpose=purpose,
        quantity=quantity,
        status="Active"
    )

    booking_list.append(new_booking.display_booking_details())

    selected_equipment["available_quantity"] = available_quantity - quantity

    if selected_equipment["available_quantity"] == 0:
        selected_equipment["status"] = "unavailable"
    else:
        selected_equipment["status"] = "available"

    save_bookings(booking_list)
    save_equipment(equipment_list)

    return redirect(url_for("home", message=f"Booking {booking_id} created successfully."))


@app.route("/return/<booking_id>", methods=["POST"])
def return_equipment(booking_id):
    booking_list = read_bookings()
    equipment_list = read_equipment()
    selected_booking = None

    for booking in booking_list:
        if booking.get("booking_id", "").lower() == booking_id.lower():
            selected_booking = booking
            break

    if selected_booking is None:
        return redirect(url_for("home", message="Booking not found."))

    if selected_booking.get("status") not in {"Active", "Overdue"}:
        return redirect(url_for("home", message="This booking has already been returned."))

    equipment_id = selected_booking.get("equipment", "")
    returned_quantity = selected_booking.get("quantity", 1)

    for equipment in equipment_list:
        saved_id = equipment.get("equipment_id", equipment.get("id", ""))

        if saved_id.lower() == equipment_id.lower():
            total_quantity = equipment.get("quantity", 1)
            available_quantity = equipment.get("available_quantity", total_quantity)
            equipment["available_quantity"] = min(total_quantity, available_quantity + returned_quantity)
            equipment["status"] = "available"
            break

    selected_booking["status"] = "Returned"

    save_bookings(booking_list)
    save_equipment(equipment_list)

    return redirect(url_for("home", message=f"Booking {booking_id} returned successfully."))


if __name__ == "__main__":
    app.run(debug=True)
