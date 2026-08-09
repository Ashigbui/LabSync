class Equipment:
    VALID_STATUSES = {"available", "unavailable", "damaged", "maintenance"}

    def __init__(self, equipment_id, name, category, laboratory, quantity, available_quantity, status, safety_instructions, maintenance_history=None, booking_history=None):
        self.equipment_id = equipment_id
        self.name = name
        self.category = category
        self.laboratory = laboratory
        self.quantity = quantity
        self.available_quantity = available_quantity
        self.status = status
        self.safety_instructions = safety_instructions
        self.maintenance_history = maintenance_history or []
        self.booking_history = booking_history or []
        self.damage_history = []

    def check_availability(self):
        return self.status == "available" and self.available_quantity > 0

    def update_status(self, new_status):
        if new_status not in self.VALID_STATUSES:
            return "Invalid status. Use available, unavailable, damaged, or maintenance."

        self.status = new_status
        return f"Status updated to {new_status}."

    def reduce_available_quantity(self, amount):
        if amount <= 0:
            return "Amount must be greater than zero."

        if amount > self.available_quantity:
            return "Not enough equipment is available."

        self.available_quantity -= amount

        if self.available_quantity == 0:
            self.status = "unavailable"

        return f"Quantity reduced by {amount}. Remaining quantity: {self.available_quantity}."

    def increase_available_quantity(self, amount):
        if amount <= 0:
            return "Amount must be greater than zero."

        if self.available_quantity + amount > self.quantity:
            return "Available quantity cannot exceed total quantity."

        self.available_quantity += amount

        if self.available_quantity > 0:
            self.status = "available"

        return f"Quantity increased by {amount}. Available quantity: {self.available_quantity}."

    def update_safety_instructions(self, new_instructions):
        if not new_instructions:
            return "Safety instructions cannot be empty."

        self.safety_instructions = new_instructions
        return "Safety instructions updated successfully."

    def record_damage(self, damage_details):
        if not damage_details:
            return "Damage details are required."

        damage_record = {"details": damage_details, "status": "reported"}
        self.damage_history.append(damage_record)
        self.status = "damaged"

        return "Damage recorded successfully."

    def send_for_maintenance(self, maintenance_details):
        if not maintenance_details:
            return "Maintenance details are required."

        maintenance_record = {"details": maintenance_details, "status": "in progress"}
        self.maintenance_history.append(maintenance_record)
        self.status = "maintenance"
        self.available_quantity = 0

        return "Equipment sent for maintenance."

    def display_details(self):
        return {"equipment_id": self.equipment_id, "name": self.name, "category": self.category, "laboratory": self.laboratory, "quantity": self.quantity, "available_quantity": self.available_quantity, "status": self.status, "safety_instructions": self.safety_instructions, "maintenance_history": self.maintenance_history, "booking_history": self.booking_history, "damage_history": self.damage_history}
