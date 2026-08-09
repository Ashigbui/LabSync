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
        print(f"{equipment} added to {self.lab_name}.")
    
    def remove_equipment(self, equipment):
        if equipment in self.equipment_list:
            self.equipment_list.remove(equipment)
            print(f"{equipment} removed from {self.equipment_list}.")
        else:
            print(f"{equipmnt} not found in {self.equipment_list}.")
    
    def search_equipment(self, equipment_name):
        if equipment_name in self.equipment_list:
            print("{equipment_name} is available in {self.equipment_list}.")
            return True
        else:
            print("{equipment_name} not found in {self.equipment_list}.")
            return False
        
    def view_availability(self):
        if self.equipment_list:
            print(f"Available equipment in {self.lab_name}:")
            for equipment in self.equipment_list:
                print(f"- {equipment}")
        else:
            print(f"No equipment currently available in {self.lab_name}.")
    
    def display_lab_info(self):
        print(f"""
        Lab ID: {self.lab_id}
        Lab Name: {self.lab_name}
        Location: {self.location}
        Technician: {self.technician}
        Opening Hours: {self.opening_hours}
        Closing Hours: {self.closing_hours}
        Equipment List: {', '.join(self.equipment_list) if self.equipment_list else 'None'}
        """)
    
