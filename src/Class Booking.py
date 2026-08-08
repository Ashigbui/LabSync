import datetime

class Booking:
    def__init__(self, booking_id, student, equipment, booking_date, start_time, return_time, purpose):
        self.__booking_id = booking_id
        self.__student = student
        self.__equipment = equipment
        self.__booking_date = booking_date
        self.__start_time = start_time
        self.__return_time = return_time
        self.__purpose = purpose
        self.__status = "Pending"
        self.__admin comment = ""

     def get_status(self):
         return self.__status

     def get_booking_id(self):
         return self.__booking_id

     def submit_request(self):
         self.__status = "Pending"
         print(f"Booking {self.__booking_id} has been submitted for {self.__equipment} by {self.__student}>")

     def approve(self, comment=""):
         self.__status = "Approved"
         self.__admin_comment = comment
         print(f"Booking {self.__booking_id} has been approved. {comment}")

     def deny(self, comment=""):
         self.__status = "Denied"
         self.__admin_comment = comment
         print(f"Booking {self.__booking_id} has been denied. {comment}")

     def cancel(self):
         self.__status = "Cancelled"
         print(f"Booking {self.__booking_id} has been cancelled.")

     def mark_active(self):
         if self.__status == "Approved":
             self.__status = "Active"
             print(f"Booking {self.__booking_id} is active.")
         else:
             print("Booking must be approved before itis active")
             

    def mark_returned(self):
         if self.__status == "Active":
            self.__status = "Returned"
            print(f"Equipment {self.__equipment} returned for booking {self.__booking_id}.")
        else:
            print("Booking must be active before returning equipment.")

    def check_overdue(self):
        today = datetime.date.today()
        if self.__status == "Active" and today > self.__return_time:
            self.__status = "Overdue"
            print(f"Booking {self.__booking_id} is overdue!")
        else:
            print(f"Booking {self.__booking_id} is not overdue.")

    def display_booking_details(self):
        print(f"""
        Booking ID: {self.__booking_id}
        Student: {self.__student}
        Equipment: {self.__equipment}
        Booking Date: {self.__booking_date}
        Start Time: {self.__start_time}
        Return Time: {self.__return_time}
        Purpose: {self.__purpose}
        Status: {self.__status}
        Admin Comment: {self.__admin_comment}
        """)   
            
             
         
