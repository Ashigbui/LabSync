class MaintenanceRecord:
    def __init__(self, maintenance_id, equipment, fault_description, date_started, expected_completion_date, date_completed, technician_name, status, cost):
        self.maintenance_id = maintenance_id
        self.equipment = equipment
        self.fault_description = fault_description
        self.date_started = date_started
        self.expected_completion_date = expected_completion_date
        self.date_completed = date_completed
        self.technician_name = technician_name
        self.status = status
        self.cost = cost

    def start_maintenance(self):
       self.status = "In Progress"

    def complete_maintenance(self):
        self.status = "Completed"

    def get_record(self):
        return 
            "equipment_id": self.equipment_id,
            "problem": self.problem,
            "technician": self.technician,
            "status": self.status
        
        

    def update_status(self):
        pass

    def complete_maintenance(self):
        pass

    def display_record(self):
        pass
