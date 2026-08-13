import datetime


class Booking:
    VALID_STATUSES = {"Pending", "Approved", "Denied", "Cancelled", "Active", "Returned", "Overdue"}

    def __init__(self, booking_id, student, equipment, booking_date, start_time, return_time, purpose, quantity=1, status="Pending", admin_comment=""):
        self.__booking_id = booking_id
        self.__student = student
        self.__equipment = equipment
        self.__booking_date = booking_date
        self.__start_time = start_time
        self.__return_time = return_time
        self.__purpose = purpose
        self.__quantity = quantity
        self.__status = status
        self.__admin_comment = admin_comment

    def get_status(self):
        return self.__status

    def get_booking_id(self):
        return self.__booking_id

    def submit_request(self):
        self.__status = "Pending"
        return f"Booking {self.__booking_id} was submitted by {self.__student}."

    def approve(self, comment=""):
        self.__status = "Approved"
        self.__admin_comment = comment
        return f"Booking {self.__booking_id} was approved."

    def deny(self, comment=""):
        self.__status = "Denied"
        self.__admin_comment = comment
        return f"Booking {self.__booking_id} was denied."

    def cancel(self):
        if self.__status in {"Returned", "Cancelled"}:
            return "This booking cannot be cancelled."

        self.__status = "Cancelled"
        return f"Booking {self.__booking_id} was cancelled."

    def mark_active(self):
        if self.__status != "Approved":
            return "Booking must be approved before it becomes active."

        self.__status = "Active"
        return f"Booking {self.__booking_id} is active."

    def mark_returned(self):
        if self.__status not in {"Active", "Overdue"}:
            return "Booking must be active before equipment is returned."

        self.__status = "Returned"
        return f"Equipment for booking {self.__booking_id} was returned."

    def check_overdue(self):
        if isinstance(self.__return_time, str):
            return_date = datetime.date.fromisoformat(self.__return_time)
        else:
            return_date = self.__return_time

        if self.__status == "Active" and datetime.date.today() > return_date:
            self.__status = "Overdue"
            return True

        return False

    def display_booking_details(self):
        return {
            "booking_id": self.__booking_id,
            "student": self.__student,
            "equipment": self.__equipment,
            "booking_date": str(self.__booking_date),
            "start_time": str(self.__start_time),
            "return_time": str(self.__return_time),
            "purpose": self.__purpose,
            "quantity": self.__quantity,
            "status": self.__status,
            "admin_comment": self.__admin_comment
        }
