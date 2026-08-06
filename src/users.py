class User:
  def __init__(self, user_id, name, email, password, role):
      self.user_id = user_id
      self.name = name
      self.email = email
      self.__password = password
      self.role = role

  def register(self):
      pass
  
  def login(self):
      pass
  
  def confirm_registration(self):
      pass
  
  def view_profile(self):
      pass
    
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
      pass 
  
  def view_equipment(self, equipment_id):
      pass
  
  def request_booking(self, equipment_id):
      pass
  
  def cancel_booking(self, booking_id):
      pass
  
  def return_equipment(self, equipment_id):
      pass
  
  def report_damage(self, equipment_id):
      pass
  
  def view_booking_history(self):
      pass
  
  def view_safety_guidelines(self):
      pass
  
class Admin(User):
  def __init__(self, user_id, name, email, password, staff_id, manage_laboratory, notifications):
      super().__init__(user_id, name, email, password, "admin"):
      self.staff_id = staff_id
      self.manage_laboratory = manage_laboratory
      self.notifications = notifications
            
  def add_equipment(self, equipment_name, equipment_type, quantity, safety_guidelines):
      pass
  
  def update_equipment(self, equipment_id, updated_info):
      pass
  
  def remove_equipment(self, equipment_id):
      pass
  
  def approve_booking(self, booking_id):
      pass
  
  def deny_booking(self, booking_id):
      pass
  
  def update_safety_guidelines(self, equipment_id, updated_guidelines):
      pass
  
  def view_pending_requests(self):
      pass
  
  def view_overdue_equipment(self):
      pass
  
  def flag_student(self, student_id):
      pass
  
  def schedule_maintenance(self, equipment_id, maintenance_date):
      pass
  
  def generate_report(self, report_type):
      pass
  
  
  
            
        
