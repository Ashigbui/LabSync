class Notification:
    def __init__(self, notification_id, recipient, message, date_created, notification_type, is_read=False):
        self.notification_id = notification_id
        self.recipient = recipient
        self.message = message
        self.date_created = date_created
        self.notification_type = notification_type
        self.is_read = is_read

    def send(self):
        pass

    def mark_as_read(self):
       pass
       
