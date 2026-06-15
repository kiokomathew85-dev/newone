import uuid

class Patient:
    def __init__(self, name, phone_number, date_of_birth, height="", weight=""):
        self.patient_id = "P-" + str(uuid.uuid4())[:6].upper()
        self.name = name
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
        self.height = height
        self.weight = weight

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "phone_number": self.phone_number,
            "date_of_birth": self.date_of_birth,
            "height": self.height,
            "weight": self.weight
        }
