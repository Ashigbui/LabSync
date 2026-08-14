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


def find_equipment(equipment_list, equipment_id):
    for equipment in equipment_list:
        saved_id = equipment.get("equipment_id", equipment.get("id", ""))

        if saved_id.lower() == equipment_id.lower():
            return equipment

    return None


def find_booking(booking_list, booking_id):
    for booking in booking_list:
        if booking.get("booking_id", "").lower() == booking_id.lower():
            return booking

    return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/student")
def student_portal():
    return render_template(
        "student.html",
        equipment_list=read_equipment(),
        booking_list=read_bookings()
    )


@app.route("/admin")
def admin_portal():
    return render_template(
        "admin.html",
        equipment_list=read_equipment(),
        booking_list=read_bookings()
    )


@app.route("/add", methods=["POST"])
def add_equipment():
    equipment_id = request.form.get("equipment_id", "").strip()
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    quantity_text = request.form.get("quantity", "").strip()

    if not equipment_id or not name or not category or not quantity_text:
        return redirect(url_for("admin_portal", message="Please complete every equipment field."))

    try:
        quantity = int(quantity_text)

        if quantity <= 0:
            raise ValueError
    except ValueError:
        return redirect(url_for("admin_portal", message="Quantity must be a positive whole number."))

    equipment_list = read_equipment()

    if find_equipment(equipment_list, equipment_id):
        return redirect(url_for("admin_portal", message="That equipment ID already exists."))

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

    return redirect(url_for("admin_portal", message="Equipment added successfully."))


@app.route("/delete/<equipment_id>", methods=["POST"])
def delete_equipment(equipment_id):
    equipment_list = read_equipment()
    booking_list = read_bookings()

    for booking in booking_list:
        if booking.get("equipment", "").lower() == equipment_id.lower() and booking.get("status") in {"Pending", "Approved", "Active", "Overdue"}:
            return redirect(url_for("admin_portal", message="This equipment has an unfinished booking and cannot be deleted."))

    updated_list = [
        equipment
        for equipment in equipment_list
        if equipment.get("equipment_id", equipment.get("id", "")).lower() != equipment_id.lower()
    ]

    save_equipment(updated_list)
    return redirect(url_for("admin_portal", message="Equipment deleted successfully."))


@app.route("/book", methods=["POST"])
def book_equipment():
    student = request.form.get("student", "").strip()
    equipment_id = request.form.get("booking_equipment", "").strip()
    quantity_text = request.form.get("booking_quantity", "").strip()
    return_date = request.form.get("return_date", "").strip()
    purpose = request.form.get("purpose", "").strip()

    if not student or not equipment_id or not quantity_text or not return_date or not purpose:
        return redirect(url_for("student_portal", message="Please complete every booking field."))

    try:
        quantity = int(quantity_text)

        if quantity <= 0:
            raise ValueError
    except ValueError:
        return redirect(url_for("student_portal", message="Booking quantity must be a positive whole number."))

    try:
        chosen_return_date = date.fromisoformat(return_date)

        if chosen_return_date < date.today():
            return redirect(url_for("student_portal", message="The return date cannot be in the past."))
    except ValueError:
        return redirect(url_for("student_portal", message="Please enter a valid return date."))

    equipment_list = read_equipment()
    selected_equipment = find_equipment(equipment_list, equipment_id)

    if selected_equipment is None:
        return redirect(url_for("student_portal", message="The selected equipment was not found."))

    available_quantity = selected_equipment.get("available_quantity", selected_equipment.get("quantity", 1))

    if quantity > available_quantity:
        return redirect(url_for("student_portal", message="There is not enough equipment available."))

    booking_list = read_bookings()
    booking_number = len(booking_list) + 1
    booking_id = f"BK{booking_number:03d}"
    existing_ids = {booking.get("booking_id", "") for booking in booking_list}

    while booking_id in existing_ids:
        booking_number += 1
        booking_id = f"BK{booking_number:03d}"

    new_booking = Booking(
        booking_id=booking_id,
        student=student,
        equipment=equipment_id,
        booking_date=date.today(),
        start_time=date.today(),
        return_time=chosen_return_date,
        purpose=purpose,
        quantity=quantity,
        status="Pending"
    )

    booking_list.append(new_booking.display_booking_details())
    save_bookings(booking_list)

    return redirect(url_for("student_portal", message=f"Booking {booking_id} was submitted for approval."))


@app.route("/approve/<booking_id>", methods=["POST"])
def approve_booking(booking_id):
    booking_list = read_bookings()
    equipment_list = read_equipment()
    booking = find_booking(booking_list, booking_id)

    if booking is None:
        return redirect(url_for("admin_portal", message="Booking not found."))

    if booking.get("status") != "Pending":
        return redirect(url_for("admin_portal", message="Only pending bookings can be approved."))

    equipment = find_equipment(equipment_list, booking.get("equipment", ""))

    if equipment is None:
        return redirect(url_for("admin_portal", message="The equipment for this booking was not found."))

    requested_quantity = booking.get("quantity", 1)
    available_quantity = equipment.get("available_quantity", equipment.get("quantity", 1))

    if requested_quantity > available_quantity:
        return redirect(url_for("admin_portal", message="There is not enough equipment available to approve this booking."))

    equipment["available_quantity"] = available_quantity - requested_quantity
    equipment["status"] = "unavailable" if equipment["available_quantity"] == 0 else "available"
    booking["status"] = "Active"
    booking["admin_comment"] = request.form.get("comment", "").strip()

    save_equipment(equipment_list)
    save_bookings(booking_list)

    return redirect(url_for("admin_portal", message=f"Booking {booking_id} was approved."))


@app.route("/deny/<booking_id>", methods=["POST"])
def deny_booking(booking_id):
    booking_list = read_bookings()
    booking = find_booking(booking_list, booking_id)

    if booking is None:
        return redirect(url_for("admin_portal", message="Booking not found."))

    if booking.get("status") != "Pending":
        return redirect(url_for("admin_portal", message="Only pending bookings can be denied."))

    booking["status"] = "Denied"
    booking["admin_comment"] = request.form.get("comment", "").strip()
    save_bookings(booking_list)

    return redirect(url_for("admin_portal", message=f"Booking {booking_id} was denied."))


@app.route("/return/<booking_id>", methods=["POST"])
def return_equipment(booking_id):
    booking_list = read_bookings()
    equipment_list = read_equipment()
    booking = find_booking(booking_list, booking_id)

    if booking is None:
        return redirect(url_for("admin_portal", message="Booking not found."))

    if booking.get("status") not in {"Active", "Overdue"}:
        return redirect(url_for("admin_portal", message="Only active or overdue bookings can be returned."))

    equipment = find_equipment(equipment_list, booking.get("equipment", ""))

    if equipment is not None:
        total_quantity = equipment.get("quantity", 1)
        available_quantity = equipment.get("available_quantity", total_quantity)
        returned_quantity = booking.get("quantity", 1)
        equipment["available_quantity"] = min(total_quantity, available_quantity + returned_quantity)
        equipment["status"] = "available"

    booking["status"] = "Returned"

    save_equipment(equipment_list)
    save_bookings(booking_list)

    return redirect(url_for("admin_portal", message=f"Booking {booking_id} was returned successfully."))


if __name__ == "__main__":
    app.run(debug=True)
