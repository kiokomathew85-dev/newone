import storage
from session import Session
from diagnosis import Diagnosis

# this holds the currently logged in doctor
logged_in_doctor = None


# ============================================================
# AUTH
# ============================================================

def login():
    print("\n--- LOGIN ---")
    doctor_id = input("Enter Doctor ID: ").strip()
    password = input("Enter Password: ").strip()

    doctor = storage.login_doctor(doctor_id, password)
    if doctor:
        print(f"\nWelcome Dr. {doctor.name}!")
        return doctor
    else:
        print("Wrong ID or password. Please try again.")
        return None

def signup():
    print("\n--- SIGN UP ---")
    name = input("Full Name: ").strip()
    doctor_id = input("Choose a Doctor ID: ").strip()
    password = input("Choose a Password: ").strip()

    if name == "" or doctor_id == "" or password == "":
        print("All fields are required.")
        return None

    doctor = storage.register_doctor(name, doctor_id, password)
    return doctor


def auth_screen():
    while True:
        print("\n=============================")
        print(" Doctor Portal")
        print("=============================")
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            doctor = login()
            if doctor:
                return doctor
        elif choice == "2":
            doctor = signup()
            if doctor:
                return doctor
        elif choice == "3":
            print("Goodbye!")
            exit()
        else:
            print("Please enter 1, 2 or 3.")


# ============================================================
# MENU 1 - DIAGNOSE PATIENT
# ============================================================

def diagnose_patient(doctor):
    print("\n--- DIAGNOSE PATIENT ---")

    patients = storage.get_all_patients()
    if len(patients) == 0:
        print("No patients found. Please create a patient first.")
        return

    print("\nSelect a patient:")
    for i, p in enumerate(patients, 1):
        print(f"{i}. {p.name} (ID: {p.patient_id})")

    try:
        choice = int(input("Enter number: "))
        if choice < 1 or choice > len(patients):
            print("Invalid choice.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    patient = patients[choice - 1]
    print(f"\nStarting diagnosis for: {patient.name}")

    # create and start session
    session = Session(patient.patient_id, doctor.doctor_id)
    session.start_session()
    session.save()

    # run diagnosis
    diag = Diagnosis(session.session_id, patient.patient_id, doctor.doctor_id)
    success = diag.enter_symptoms()

    if not success:
        print("Diagnosis was not completed.")
        session.end_session()
        session.save()
        return

    # update session with diagnosis
    session.diagnosis = diag.disease

    # doctor enters notes
    print("\nEnter session notes (press Enter to skip):")
    notes = input("> ").strip()
    if notes != "":
        session.add_notes(notes)

    # end session
    session.end_session()
    session.save()

    # show and save diagnosis
    diag.show_summary()
    storage.save_diagnosis(diag.to_dict())
    print("\nDiagnosis saved successfully.")


# ============================================================
# MENU 2 - CREATE PATIENT
# ============================================================

def create_patient(doctor):
    print("\n--- CREATE PATIENT ---")

    name = input("Patient Name: ").strip()
    phone = input("Phone Number: ").strip()
    dob = input("Date of Birth (YYYY-MM-DD): ").strip()
    height = input("Height in cm (press Enter to skip): ").strip()
    weight = input("Weight in kg (press Enter to skip): ").strip()

    if name == "" or phone == "" or dob == "":
        print("Name, phone and date of birth are required.")
        return

    from patient import Patient
    patient = Patient(name, phone, dob, height, weight)
    storage.save_patient(patient)

    print(f"\nPatient created!")
    print(f"Name      : {patient.name}")
    print(f"Patient ID: {patient.patient_id}")


# ============================================================
# MENU 3 - VIEW PATIENT HISTORY
# ============================================================

def view_patient_history(doctor):
    print("\n--- VIEW PATIENT HISTORY ---")

    search = input("Search patient by name (press Enter to list all): ").strip()

    if search != "":
        patients = storage.search_patients_by_name(search)
    else:
        patients = storage.get_all_patients()

    if len(patients) == 0:
        print("No patients found.")
        return

    print("\nPatients:")
    for i, p in enumerate(patients, 1):
        print(f"{i}. {p.name} (ID: {p.patient_id})")

    try:
        choice = int(input("\nSelect patient number to view history: "))
        if choice < 1 or choice > len(patients):
            print("Invalid choice.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    patient = patients[choice - 1]

    print("\n" + "=" * 40)
    print("PATIENT DETAILS")
    print("=" * 40)
    print("Name       :", patient.name)
    print("ID         :", patient.patient_id)
    print("Phone      :", patient.phone_number)
    print("D.O.B      :", patient.date_of_birth)
    print("Height     :", patient.height if patient.height else "Not provided")
    print("Weight     :", patient.weight if patient.weight else "Not provided")

    # show sessions
    sessions = storage.get_patient_sessions(patient.patient_id)
    print(f"\nSessions ({len(sessions)}):")
    print("-" * 40)
    if len(sessions) == 0:
        print("No sessions recorded.")
    for s in sessions:
        print(f"Date      : {s['date_time']}")
        print(f"Status    : {s['status']}")
        print(f"Diagnosis : {s['diagnosis']}")
        print(f"Notes     : {s['notes'] if s['notes'] else 'None'}")
        print("-" * 40)

    # show diagnoses
    diagnoses = storage.get_patient_diagnoses(patient.patient_id)
    print(f"\nDiagnoses ({len(diagnoses)}):")
    print("-" * 40)
    if len(diagnoses) == 0:
        print("No diagnoses recorded.")
    for d in diagnoses:
        print(f"Disease   : {d['disease']}")
        syms = d['symptoms']
        if isinstance(syms, list):
            syms = ", ".join(syms)
        print(f"Symptoms  : {syms}")
        print(f"Medication: {d['medication']}")
        print("-" * 40)


# ============================================================
# MENU 4 - UPDATE PATIENT DETAILS
# ============================================================

def update_patient(doctor):
    print("\n--- UPDATE PATIENT DETAILS ---")

    patients = storage.get_all_patients()
    if len(patients) == 0:
        print("No patients found.")
        return

    print("\nPatients:")
    for i, p in enumerate(patients, 1):
        print(f"{i}. {p.name} (ID: {p.patient_id})")

    try:
        choice = int(input("\nSelect patient to update: "))
        if choice < 1 or choice > len(patients):
            print("Invalid choice.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    patient = patients[choice - 1]
    print(f"\nEditing: {patient.name}")
    print("Press Enter to keep the current value.\n")

    new_name = input(f"Name [{patient.name}]: ").strip()
    new_phone = input(f"Phone [{patient.phone_number}]: ").strip()
    new_dob = input(f"Date of Birth [{patient.date_of_birth}]: ").strip()
    new_height = input(f"Height [{patient.height}] cm: ").strip()
    new_weight = input(f"Weight [{patient.weight}] kg: ").strip()

    storage.update_patient(patient.patient_id, new_name, new_phone, new_dob, new_height, new_weight)


# ============================================================
# MENU 5 - DELETE PATIENT
# ============================================================

def delete_patient_ui(doctor):
    print("\n--- DELETE PATIENT record ---")
    
    patients = storage.get_all_patients()
    if len(patients) == 0:
        print("No patients found.")
        return

    print("\nSelect a patient to delete:")
    for i, p in enumerate(patients, 1):
        print(f"{i}. {p.name} (ID: {p.patient_id})")

    try:
        choice = int(input("\nEnter number to delete (or 0 to cancel): "))
        if choice == 0:
            return
        if choice < 1 or choice > len(patients):
            print("Invalid choice.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    patient = patients[choice - 1]
    
    confirm = input(f"Are you sure you want to delete {patient.name} (ID: {patient.patient_id})? (y/n): ").lower().strip()
    if confirm == 'y':
        from patient import PatientDeleter
        if PatientDeleter.delete_patient(patient.patient_id):
            print(f"Patient {patient.name} deleted successfully.")
        else:
            print("Failed to delete patient.")
    else:
        print("Deletion cancelled.")


# ============================================================
# MENU 6 - UPDATE DOCTOR DETAILS
# ============================================================

def update_doctor_details(doctor):
    print("\n--- UPDATE MY DETAILS ---")
    print(f"Current Name: {doctor.name}")
    print("Press Enter to keep the current value.\n")

    new_name = input(f"New Name [{doctor.name}]: ").strip()
    new_password = input("New Password (press Enter to skip): ").strip()

    storage.update_doctor(doctor.doctor_id, new_name, new_password)

    # update the name in memory too if changed
    if new_name != "":
        doctor.name = new_name

    print("If you changed your password, please log in again.")
    if new_password != "":
        return "logout"
    return None


# ============================================================
# MAIN MENU
# ============================================================

def main_menu(doctor):
    while True:
        print("\n=============================")
        print(f"  MAIN MENU - Dr. {doctor.name}")
        print("=============================")
        print("1. Diagnose Patient")
        print("2. Create Patient")
        print("3. View Patient History")
        print("4. Update Patient Details")
        print("5. Delete Patient Record")
        print("6. Update My Details")
        print("7. Logout")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            diagnose_patient(doctor)
        elif choice == "2":
            create_patient(doctor)
        elif choice == "3":
            view_patient_history(doctor)
        elif choice == "4":
            update_patient(doctor)
        elif choice == "5":
            delete_patient_ui(doctor)
        elif choice == "6":
            result = update_doctor_details(doctor)
            if result == "logout":
                print("Please log in again with your new password.")
                return
        elif choice == "7":
            print(f"\nLogging out. Goodbye Dr. {doctor.name}!")
            return
        else:
            print("Please enter a number between 1 and 7.")


# ============================================================
# RUN THE PROGRAM
# ============================================================

while True:
    doctor = auth_screen()
    main_menu(doctor)
