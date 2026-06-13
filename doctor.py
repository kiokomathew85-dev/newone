import functools
import getpass
import sys
from datetime import datetime

def require_doctor_privileges(func):
    @functools.wraps(func)
    def wrapper(instance, *args, **kwargs):
        role = getattr(instance, "role", None)
        if not role or role.lower() != "admin":
            raise PermissionError("Access Denied: Doctor privileges required.")
        return func(instance, *args, **kwargs)
    return wrapper

class User:
    def __init__(self, username, user_id, password, role):
        self._username = username       
        self._user_id = user_id         
        self._password = password
        self._role = role

    @property
    def username(self):
        return self._username

    @property
    def user_id(self):
        return self._user_id

    @property
    def role(self):
        return self._role

    def check_password(self, password_input):
        return self._password == password_input

class Doctor(User):
    def __init__(self, name, doctor_id, password):
        super().__init__(username=name, user_id=doctor_id, password=password, role="Admin")

    @property
    def name(self):
        return self.username

    @property
    def doctor_id(self):
        return self.user_id

    @require_doctor_privileges
    def view_patient_history(self, patient_id, storage_engine):
        patient = storage_engine.load_patient(patient_id)
        if not patient:
            return None
        return patient.fetch_patient_history()

    @require_doctor_privileges
    def diagnosis_patient(self, session_id, patient_id, symptoms, disease, prevention, medication, storage_engine):
        diagnosis_data = {
            "session_id": session_id,
            "patient_id": patient_id,
            "doctor_id": self.doctor_id,
            "symptoms": symptoms,
            "disease": disease,
            "prevention": prevention,
            "medication": medication,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        storage_engine.save_diagnosis(diagnosis_data)
        return diagnosis_data

    @require_doctor_privileges
    def update_patient(self, patient_id, updated_fields, storage_engine):
        patient = storage_engine.load_patient(patient_id)
        if not patient:
            raise ValueError(f"Patient with ID {patient_id} not found.")

        allowed_fields = ["name", "date_of_birth", "height", "weight", "phone_number"]
        for field, value in updated_fields.items():
            if field in allowed_fields:
                setattr(patient, field, value)

        storage_engine.save_patient(patient)
        return True

    @require_doctor_privileges
    def delete_patient(self, patient_id, storage_engine):
        return storage_engine.delete_patient(patient_id)

def doctor_login_form(auth_system):
    print("=" * 45)
    print("       CLINIC MANAGEMENT SYSTEM LOGIN        ")
    print("=" * 45)
    
    attempts = 3
    while attempts > 0:
        print(f"\n[Remaining Login Attempts: {attempts}]")
        doc_id = input("Enter Doctor ID: ").strip()
        password = getpass.getpass("Enter Secret Password: ")
        
        doctor_session = auth_system.authenticate_doctor(doc_id, password)
        
        if doctor_session:
            print(f"\n[+] Access Granted. Welcome, Dr. {doctor_session.name}!")
            return doctor_session
        else:
            print("[!] Invalid Doctor ID or Password match.")
            attempts -= 1
            
    print("\n[!!!] Maximum authentication attempts reached. Exiting program.")
    sys.exit()
