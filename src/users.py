class User:
    registered_emails = []

    def __init__(self, user_id, name, email, password, role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.__password = password
        self.role = role
        self.is_registered = False

    def register(self):
        if self.email in User.registered_emails:
            return "Registration failed: Email already exists."

        User.registered_emails.append(self.email)
        self.is_registered = True

        return "Registration successful."

    def login(self, email, password):
        if not self.is_registered:
            return "Login failed: User is not registered."

        if self.email == email and self.__password == password:
            return "Login successful."

        return "Login failed: Incorrect email or password."

    def confirm_registration(self):
        return self.is_registered

    def view_profile(self):
        if not self.is_registered:
            return "Profile unavailable: User is not registered."

        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role
        }
    
class Student(User):
  def __init__(self, user_id, name, email, password, program, yeargroup, booking_history, overdue_count, damage_count, flagged_count):
      super().__init__(user_id, name, email, password, "student")
      self.program = program
      self.yeargroup = yeargroup
      self.booking_history = booking_history
      self.overdue_count = overdue_count
      self.damage_count = damage_count
      self.flagged_count = flagged_count
      
  def search_equipment(self, equipment_name):
        if not self.is_registered:
            return "Search unavailable: User is not registered."

        return f"Searching for equipment: {equipment_name}"

  def view_equipment(self, equipment_id):
        if not self.is_registered:
            return "View unavailable: User is not registered."

        return f"Viewing equipment: {equipment_id}"

  def request_booking(self, equipment_id):
        if not self.is_registered:
            return "Booking request unavailable: User is not registered."

        booking = {"equipment_id": equipment_id,"status": "pending"}
        self.booking_history.append(booking)

        return f"Booking requested for equipment: {equipment_id}"

  def cancel_booking(self, booking_id):
        if not self.is_registered:
            return "Cancel booking unavailable: User is not registered."

        if not 0 <= booking_id < len(self.booking_history):
            return "Cancellation failed: Booking not found."

        booking = self.booking_history[booking_id]

        if booking["status"] != "pending":
            return "Cancellation failed: Only pending bookings can be cancelled."

        booking["status"] = "cancelled"
        return f"Booking {booking_id} cancelled successfully."

  def return_equipment(self, equipment_id):
        if not self.is_registered:
            return "Return equipment unavailable: User is not registered."

        return f"Equipment {equipment_id} returned successfully."

  def report_damage(self, equipment_id):
        if not self.is_registered:
            return "Report damage unavailable: User is not registered."

        self.damage_count += 1
        return f"Damage reported for equipment: {equipment_id}"

  def view_booking_history(self):
        if not self.is_registered:
            return "Booking history unavailable: User is not registered."

        return self.booking_history

def view_safety_guidelines(self):
        if not self.is_registered:
            return "Safety guidelines unavailable: User is not registered."

        return "Viewing safety guidelines."
    
class Admin(User):
    def __init__(self, user_id, name, email, password, staff_id, manage_laboratory, notifications=None,):
        super().__init__(user_id, name, email, password, "admin")
        self.staff_id = staff_id
        self.manage_laboratory = manage_laboratory
        self.notifications = notifications or []
        self.equipment = {}
        self.booking_requests = {}
        self.overdue_equipment = []
        self.flagged_students = []
        self.maintenance_schedule = []
        self.reports = []
        self.next_equipment_id = 1

    def _check_registration(self):
        if not self.is_registered:
            return "Action unavailable: Admin is not registered."
        return None

    def add_equipment(self, equipment_name, equipment_type, quantity, safety_guidelines):
        error = self._check_registration()
        if error:
            return error

        if quantity <= 0:
            return "Equipment could not be added: Quantity must be positive."

        equipment_id = self.next_equipment_id
        self.next_equipment_id += 1

        equipment = {"equipment_id": equipment_id, "name": equipment_name, "type": equipment_type, "quantity": quantity, "safety_guidelines": safety_guidelines}
        self.equipment[equipment_id] = equipment
        return equipment

    def update_equipment(self, equipment_id, updated_info):
        error = self._check_registration()
        if error:
            return error

        if equipment_id not in self.equipment:
            return "Update failed: Equipment not found."

        if not isinstance(updated_info, dict):
            return "Update failed: Updated information must be a dictionary."

        allowed_fields = {"name", "type", "quantity","safety_guidelines",}

        for field, value in updated_info.items():
            if field not in allowed_fields:
                continue

            if field == "quantity" and value <= 0:
                return "Update failed: Quantity must be positive."

            self.equipment[equipment_id][field] = value

        return "Equipment updated successfully."

    def remove_equipment(self, equipment_id):
        error = self._check_registration()
        if error:
            return error

        if equipment_id not in self.equipment:
            return "Removal failed: Equipment not found."

        removed_equipment = self.equipment.pop(equipment_id)

        return {
            "message": "Equipment removed successfully.",
            "equipment": removed_equipment,
        }

    def approve_booking(self, booking_id):
        error = self._check_registration()
        if error:
            return error

        booking = self.booking_requests.get(booking_id)

        if booking is None:
            return "Approval failed: Booking not found."

        if booking.get("status") != "pending":
            return "Approval failed: Booking has already been processed."

        booking["status"] = "approved"
        return f"Booking {booking_id} approved successfully."

    def deny_booking(self, booking_id):
        error = self._check_registration()
        if error:
            return error

        booking = self.booking_requests.get(booking_id)

        if booking is None:
            return "Denial failed: Booking not found."

        if booking.get("status") != "pending":
            return "Denial failed: Booking has already been processed."

        booking["status"] = "denied"
        return f"Booking {booking_id} denied successfully."

    def update_safety_guidelines(self, equipment_id, updated_guidelines):
        error = self._check_registration()
        if error:
            return error

        if equipment_id not in self.equipment:
            return "Update failed: Equipment not found."

        self.equipment[equipment_id]["safety_guidelines"] = updated_guidelines

        return "Safety guidelines updated successfully."

    def view_pending_requests(self):
        error = self._check_registration()
        if error:
            return error

        return {
            booking_id: booking
            for booking_id, booking in self.booking_requests.items()
            if booking.get("status") == "pending"
        }

    def view_overdue_equipment(self):
        error = self._check_registration()
        if error:
            return error

        return self.overdue_equipment

    def flag_student(self, student_id):
        error = self._check_registration()
        if error:
            return error

        if student_id in self.flagged_students:
            return "Student is already flagged."

        self.flagged_students.append(student_id)
        return f"Student {student_id} flagged successfully."

    def schedule_maintenance(
        self,
        equipment_id,
        maintenance_date,
    ):
        error = self._check_registration()
        if error:
            return error

        if equipment_id not in self.equipment:
            return "Maintenance failed: Equipment not found."

        maintenance = {"equipment_id": equipment_id, "maintenance_date": maintenance_date, "status": "scheduled"}

        self.maintenance_schedule.append(maintenance)
        return maintenance

    def generate_report(self, report_type):
        error = self._check_registration()
        if error:
            return error

        available_reports = {
            "equipment": list(self.equipment.values()),
            "bookings": list(self.booking_requests.values()),
            "overdue": self.overdue_equipment,
            "flagged_students": self.flagged_students,
            "maintenance": self.maintenance_schedule,
        }

        if report_type not in available_reports:
            return (
                "Invalid report type. Choose equipment, bookings, "
                "overdue, flagged_students, or maintenance."
            )

        report = {
            "report_type": report_type,
            "data": available_reports[report_type],
        }

        self.reports.append(report)
        return report
