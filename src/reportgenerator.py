class ReportGenerator:
    def __init__(self, bookings, equipment_records, damage_reports, maintenance_records):
        self.bookings = bookings
        self.equipment_records = equipment_records
        self.damage_reports = damage_reports
        self.maintenance_records = maintenance_records

    def generate_weekly_borrowing_report(self):
        pass

    def generate_overdue_report(self):
        pass

    def generate_damage_report(self):
       pass

    def generate_maintenance_report(self):
        pass

    def generate_high_demand_report(self):
        pass

    def export_report(self, report_type):
        pass
