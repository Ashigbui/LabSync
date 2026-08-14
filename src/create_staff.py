import json
from getpass import getpass
from pathlib import Path

from werkzeug.security import generate_password_hash


PROJECT_FOLDER = Path(__file__).resolve().parent.parent
USERS_FILE = PROJECT_FOLDER / "data" / "users.json"


def read_users():
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_users(user_list):
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(user_list, file, indent=4)


def main():
    print("Create a LabSync staff account")

    full_name = input("Full name: ").strip()
    email = input("Ashesi email: ").strip().lower()
    role = input("Role (admin/technician): ").strip().lower()
    password = getpass("Password: ")
    confirm_password = getpass("Confirm password: ")

    if not full_name or not email or not role or not password:
        print("Every field is required.")
        return

    if not email.endswith("@ashesi.edu.gh"):
        print("Please use an Ashesi email ending in @ashesi.edu.gh.")
        return

    if role not in {"admin", "technician"}:
        print("Role must be admin or technician.")
        return

    if len(password) < 8:
        print("Password must contain at least 8 characters.")
        return

    if password != confirm_password:
        print("The passwords do not match.")
        return

    user_list = read_users()

    for user in user_list:
        if user.get("email", "").lower() == email:
            print("An account with this email already exists.")
            return

    user_list.append({
        "full_name": full_name,
        "email": email,
        "password_hash": generate_password_hash(password),
        "role": role
    })

    save_users(user_list)
    print(f"{role.title()} account created successfully.")


if __name__ == "__main__":
    main()
