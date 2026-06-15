import uuid
import json
import os
from datetime import datetime

class Session:
    def __init__(self, patient_id, doctor_id, diagnosis=""):
        self.session_id = str(uuid.uuid4())
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.diagnosis = diagnosis
        self.status = "scheduled"
        self.date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.notes = ""
        self.start_time = ""
        self.end_time = ""

    def start_session(self):
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = "in-progress"
        print("Session started at:", self.start_time)

    def end_session(self):
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = "completed"
        print("Session ended at:", self.end_time)

    def add_notes(self, note):
        self.notes = note

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "diagnosis": self.diagnosis,
            "status": self.status,
            "date_time": self.date_time,
            "notes": self.notes,
            "start_time": self.start_time,
            "end_time": self.end_time
        }

    def save(self):
        # load existing sessions
        sessions = {}
        if os.path.exists("sessions.json"):
            with open("sessions.json", "r") as f:
                sessions = json.load(f)

        sessions[self.session_id] = self.to_dict()

        with open("sessions.json", "w") as f:
            json.dump(sessions, f, indent=4)
