class Equipment:
    def __init__(self, equipment_id, name, category, laboratory, quanitity, available_quantity, status, safety_instructions, maintenance_history, booking_history):
        self.equipment_id = equipment_id
        self.name = name
        self.category = category
        self.laboratory = laboratory
        self.quanitity = quanitity
        self.available_quantity = available_quantity
        self.status = status
        self.safety_instructions = safety_instructions
        self.maintenance_history = maintenance_history
        self.booking_history = booking_history
        
    def check_availability(self):
        pass
        
    def update_status(self, new_status):
        pass
        
    def reduce_available_quantity(self, amount):
       pass
    
    def increase_available_quantity(self, amount):
        pass
    
    def update_safety_instructions(self, new_instructions):
        pass
    
    def record_damage(self, damage_details):
        pass
        
    def send_for_maintenance(self, maintenance_details):
        pass
        
    def display_details(self):
        pass
    
