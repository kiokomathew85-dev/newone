import uuid

class Doctor:
    def __init__(self, name, doctor_id, password):
        self.name = name
        self.doctor_id = doctor_id
        self.password = password

    def check_password(self, password_input):
        return self.password == password_input

    def to_dict(self):
        return {
            "name": self.name,
            "doctor_id": self.doctor_id,
            "password": self.password
        }
