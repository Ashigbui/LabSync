import json
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

from equipment import Equipment


PROJECT_FOLDER = Path(__file__).resolve().parent.parent
EQUIPMENT_FILE = PROJECT_FOLDER / "data" / "equipment.json"

app = Flask(
    __name__,
    template_folder=str(PROJECT_FOLDER / "templates"),
    static_folder=str(PROJECT_FOLDER / "static")
)


def read_equipment():
    try:
        with open(EQUIPMENT_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_equipment(equipment_list):
    EQUIPMENT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(EQUIPMENT_FILE, "w", encoding="utf-8") as file:
        json.dump(equipment_list, file, indent=4)


@app.route("/")
def home():
    return render_template(
        "index.html",
        equipment_list=read_equipment()
    )


@app.route("/add", methods=["POST"])
def add_equipment():
    equipment_id = request.form.get("equipment_id", "").strip()
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    quantity_text = request.form.get("quantity", "").strip()

    if not equipment_id or not name or not category or not quantity_text:
        return redirect(url_for("home", message="Please complete every field."))

    try:
        quantity = int(quantity_text)

        if quantity <= 0:
            raise ValueError
    except ValueError:
        return redirect(
            url_for("home", message="Quantity must be a positive whole number.")
        )

    equipment_list = read_equipment()

    for saved_equipment in equipment_list:
        saved_id = saved_equipment.get(
            "equipment_id",
            saved_equipment.get("id", "")
        )

        if saved_id.lower() == equipment_id.lower():
            return redirect(
                url_for("home", message="That equipment ID already exists.")
            )

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

    updated_list = [
        equipment
        for equipment in equipment_list
        if equipment.get(
            "equipment_id",
            equipment.get("id", "")
        ).lower() != equipment_id.lower()
    ]

    save_equipment(updated_list)

    return redirect(url_for("home", message="Equipment deleted successfully."))


if __name__ == "__main__":
    app.run(debug=True)
