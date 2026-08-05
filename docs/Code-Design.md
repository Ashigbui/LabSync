CLASS 1: User class
(This should be the parent class for students and administrators)

Attributes
user_id
name
email
password
role

Methods
register()
login()
confirm_registration()
view_profile()

CLASS 2: Student class
(This inherits from User)

Additional attributes
programme
year_group
booking_history
overdue_count
damage_count
is_flagged

Methods
search_equipment()
view_equipment()
request_booking()
cancel_booking()
return_equipment()
report_damage()
view_booking_status()
view_safety_guidance()

CLASS 3: Admin class
(This also inherits from User)

Additional attributes
staff_id
managed_laboratory
notifications

Methods
add_equipment()
update_equipment()
remove_equipment()
approve_booking()
deny_booking()
update_safety_instructions()
view_pending_requests()
view_overdue_equipment()
flag_student()
schedule_maintenance()
generate_report()

CLASS 4: Fablab class
(This represents the fablab)

Attributes
lab_id
lab_name
location
equipment_list
technician
opening_time
closing_time

Methods
add_equipment()
remove_equipment()
search_equipment()
view_available_equipment()
display_lab_details()

CLASS 5: Equipment class
(This is one of the main classes)

Attributes
equipment_id
name
category
laboratory
quantity
available_quantity
status
safety_instructions
maintenance_history
booking_history

Possible statuses:
"Available"
"Booked"
"Borrowed"
"Damaged"
"Under Maintenance"

Methods
check_availability()
update_status()
reduce_available_quantity()
increase_available_quantity()
update_safety_instructions()
record_damage()
send_for_maintenance()
display_details()

CLASS 6: Booking class
(This connects a student to a piece of equipment)

Attributes
booking_id
student
equipment
booking_date
start_time
return_time
purpose
status
admin_comment

Possible booking statuses:
"Pending"
"Approved"
"Denied"
"Active"
"Returned"
"Overdue"
Methods
submit_request()
approve()
deny()
cancel()
mark_active()
mark_returned()
check_overdue()
display_booking_details()

CLASS 7: DamageReport class
(This records faults or damage)

Attributes
report_id
student
equipment
description
date_reported
severity
status
admin_comment

Methods
submit_report()
update_report()
mark_resolved()
display_report()

CLASS 8: MaintenanceRecord class
(This manages equipment undergoing repairs or servicing)

Attributes
maintenance_id
equipment
fault_description
date_started
expected_completion_date
date_completed
technician_name
status
cost

Methods
start_maintenance()
update_status()
complete_maintenance()
display_record()

CLASS 9: Notification class
(This can manage approval, denial, overdue, and maintenance messages)

Attributes
notification_id
recipient
message
date_created
notification_type
is_read

Methods
send()
mark_as_read()
display_notification()

CLASS 10: ReportGenerator class
(This handles the reports required by the administrator)

Attributes
bookings
equipment_records
damage_reports
maintenance_records

Methods
generate_weekly_borrowing_report()
generate_overdue_report()
generate_damage_report()
generate_maintenance_report()
generate_high_demand_report()
export_report()
