class Fablab:
    def __init__(self, lab_id, lab_name, lab_location, equipment_list, technician, opening_hours, closing_hours):
        self.lab_id = lab_id
        self.name = lab_name
        self.location = lab_location
        self.equipment_list = equipment_list
        self.technician = technician
        self.opening_hours = opening_hours
        self.closing_hours = closing_hours
    
    def add_equipment(self, equipment):
        self.equipment_list.append(equipment)
        pass 
    
    def remove_equipment(self, equipment):
        pass 
    
    def search_equipment(self, equipment_name):
        pass
    
    def view_availability(self):
        pass
    
    def display_lab_info(self):
        pass
    
