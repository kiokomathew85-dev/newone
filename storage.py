import json
import os
from patient import Patient
from doctor import Doctor

DOCTORS_FILE = "doctors.json"
PATIENTS_FILE = "patients.json"
DIAGNOSES_FILE = "diagnoses.json"


# ---- helper functions to load and save json files ----

def load_json(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


# ---- Doctor functions ----

def register_doctor(name, doctor_id, password):
    doctors = load_json(DOCTORS_FILE)

    if doctor_id in doctors:
        print("A doctor with that ID already exists.")
        return None

    doctors[doctor_id] = {
        "name": name,
        "doctor_id": doctor_id,
        "password": password
    }
    save_json(DOCTORS_FILE, doctors)
    print("Account created successfully!")
    return Doctor(name, doctor_id, password)

def login_doctor(doctor_id, password):
    doctors = load_json(DOCTORS_FILE)

    if doctor_id not in doctors:
        return None

    record = doctors[doctor_id]
    if record["password"] == password:
        return Doctor(record["name"], doctor_id, record["password"])
    return None

def update_doctor(doctor_id, new_name, new_password):
    doctors = load_json(DOCTORS_FILE)
    if doctor_id not in doctors:
        print("Doctor not found.")
        return

    if new_name != "":
        doctors[doctor_id]["name"] = new_name
    if new_password != "":
        doctors[doctor_id]["password"] = new_password

    save_json(DOCTORS_FILE, doctors)
    print("Your details have been updated.")


# ---- Patient functions ----

def save_patient(patient):
    patients = load_json(PATIENTS_FILE)
    patients[patient.patient_id] = patient.to_dict()
    save_json(PATIENTS_FILE, patients)

def get_all_patients():
    patients = load_json(PATIENTS_FILE)
    result = []
    for data in patients.values():
        p = Patient(
            name=data["name"],
            phone_number=data["phone_number"],
            date_of_birth=data["date_of_birth"],
            height=data.get("height", ""),
            weight=data.get("weight", "")
        )
        p.patient_id = data["patient_id"]
        result.append(p)
    return result

def get_patient_by_id(patient_id):
    patients = load_json(PATIENTS_FILE)
    if patient_id in patients:
        data = patients[patient_id]
        p = Patient(
            name=data["name"],
            phone_number=data["phone_number"],
            date_of_birth=data["date_of_birth"],
            height=data.get("height", ""),
            weight=data.get("weight", "")
        )
        p.patient_id = data["patient_id"]
        return p
    return None

def update_patient(patient_id, new_name, new_phone, new_dob, new_height, new_weight):
    patients = load_json(PATIENTS_FILE)
    if patient_id not in patients:
        print("Patient not found.")
        return

    if new_name != "":
        patients[patient_id]["name"] = new_name
    if new_phone != "":
        patients[patient_id]["phone_number"] = new_phone
    if new_dob != "":
        patients[patient_id]["date_of_birth"] = new_dob
    if new_height != "":
        patients[patient_id]["height"] = new_height
    if new_weight != "":
        patients[patient_id]["weight"] = new_weight

    save_json(PATIENTS_FILE, patients)
    print("Patient details updated.")

def search_patients_by_name(name):
    all_patients = get_all_patients()
    results = []
    for p in all_patients:
        if name.lower() in p.name.lower():
            results.append(p)
    return results

def delete_patient(patient_id):
    patients = load_json(PATIENTS_FILE)
    if patient_id in patients:
        del patients[patient_id]
        save_json(PATIENTS_FILE, patients)
        print(f"Patient with ID {patient_id} has been deleted.")
        return True
    print(f"Patient with ID {patient_id} not found.")
    return False


# ---- Diagnosis functions ----

def save_diagnosis(diagnosis_dict):
    diagnoses = load_json(DIAGNOSES_FILE)
    diagnoses[diagnosis_dict["session_id"]] = diagnosis_dict
    save_json(DIAGNOSES_FILE, diagnoses)

def get_patient_diagnoses(patient_id):
    diagnoses = load_json(DIAGNOSES_FILE)
    results = []
    for d in diagnoses.values():
        if d["patient_id"] == patient_id:
            results.append(d)
    return results


# ---- Session functions ----

def get_patient_sessions(patient_id):
    if not os.path.exists("sessions.json"):
        return []
    with open("sessions.json", "r") as f:
        sessions = json.load(f)
    results = []
    for s in sessions.values():
        if s["patient_id"] == patient_id:
            results.append(s)
    return results
