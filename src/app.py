import json
import os
from datetime import date
from functools import wraps
from pathlib import Path

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from bookings import Booking
from equipment import Equipment


PROJECT_FOLDER = Path(__file__).resolve().parent.parent
EQUIPMENT_FILE = PROJECT_FOLDER / "data" / "equipment.json"
BOOKINGS_FILE = PROJECT_FOLDER / "data" / "bookings.json"
USERS_FILE = PROJECT_FOLDER / "data" / "users.json"

app = Flask(__name__, template_folder=str(PROJECT_FOLDER / "templates"), static_folder=str(PROJECT_FOLDER / "static"))
app.secret_key = os.environ.get("LABSYNC_SECRET_KEY", "labsync-development-secret-key")


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


def read_users():
    return read_json(USERS_FILE)


def save_users(user_list):
    save_json(USERS_FILE, user_list)


def find_user(user_list, email):
    for user in user_list:
        if user.get("email", "").lower() == email.lower():
            return user

    return None


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


def login_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if "user_email" not in session:
            return redirect(url_for("login", message="Please sign in first."))

        return function(*args, **kwargs)

    return decorated_function


def student_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if "user_email" not in session:
            return redirect(url_for("login", message="Please sign in first."))

        if session.get("role") != "student":
            return redirect(url_for("admin_portal", message="This page is for students only."))

        return function(*args, **kwargs)

    return decorated_function


def staff_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if "user_email" not in session:
            return redirect(url_for("login", message="Please sign in first."))

        if session.get("role") not in {"admin", "technician"}:
            return redirect(url_for("student_portal", message="You do not have permission to access the staff portal."))

        return function(*args, **kwargs)

    return decorated_function


@app.route("/")
def home():
    if session.get("role") == "student":
        return redirect(url_for("student_portal"))

    if session.get("role") in {"admin", "technician"}:
        return redirect(url_for("admin_portal"))

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not full_name or not email or not password or not confirm_password:
        return redirect(url_for("register", message="Please complete every field."))

    if not email.endswith("@ashesi.edu.gh"):
        return redirect(url_for("register", message="Please use a valid Ashesi school email."))

    if password != confirm_password:
        return redirect(url_for("register", message="The passwords do not match."))

    if len(password) < 8:
        return redirect(url_for("register", message="Your password must contain at least 8 characters."))

    user_list = read_users()

    if find_user(user_list, email):
        return redirect(url_for("register", message="An account with this email already exists."))

    new_user = {
        "full_name": full_name,
        "email": email,
        "password_hash": generate_password_hash(password),
        "role": "student"
    }

    user_list.append(new_user)
    save_users(user_list)

    return redirect(url_for("login", message="Registration successful. You can now sign in."))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    user = find_user(read_users(), email)

    if user is None or not check_password_hash(user.get("password_hash", ""), password):
        return redirect(url_for("login", message="Incorrect email or password."))

    session.clear()
    session["user_email"] = user.get("email")
    session["full_name"] = user.get("full_name")
    session["role"] = user.get("role", "student")

    if session["role"] in {"admin", "technician"}:
        return redirect(url_for("admin_portal"))

    return redirect(url_for("student_portal"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home", message="You have signed out."))


@app.route("/student")
@student_required
def student_portal():
    all_bookings = read_bookings()
    student_bookings = [
        booking
        for booking in all_bookings
        if booking.get("student_email", "").lower() == session.get("user_email", "").lower()
    ]

    return render_template(
        "student.html",
        equipment_list=read_equipment(),
        booking_list=student_bookings,
        user_name=session.get("full_name")
    )


@app.route("/admin")
@staff_required
def admin_portal():
    return render_template(
        "admin.html",
        equipment_list=read_equipment(),
        booking_list=read_bookings(),
        user_name=session.get("full_name"),
        user_role=session.get("role")
    )


@app.route("/add", methods=["POST"])
@staff_required
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
@staff_required
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
@student_required
def book_equipment():
    equipment_id = request.form.get("booking_equipment", "").strip()
    quantity_text = request.form.get("booking_quantity", "").strip()
    return_date = request.form.get("return_date", "").strip()
    purpose = request.form.get("purpose", "").strip()

    if not equipment_id or not quantity_text or not return_date or not purpose:
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
        student=session.get("full_name"),
        equipment=equipment_id,
        booking_date=date.today(),
        start_time=date.today(),
        return_time=chosen_return_date,
        purpose=purpose,
        quantity=quantity,
        status="Pending"
    )

    booking_record = new_booking.display_booking_details()
    booking_record["student_email"] = session.get("user_email")
    booking_list.append(booking_record)
    save_bookings(booking_list)

    return redirect(url_for("student_portal", message=f"Booking {booking_id} was submitted for approval."))


@app.route("/approve/<booking_id>", methods=["POST"])
@staff_required
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
@staff_required
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
@staff_required
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
