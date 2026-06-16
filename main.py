from doctor import Doctor, load_doctors, save_doctors, doctor_login_form, run_doctor_cli


def main():
    doctors = load_doctors()

    if not doctors:
        doctors = [
            # Seed file with default doctors if none exist.
            # This is only used the first time the app runs.
            
            # Existing doctor accounts can still login with these credentials.
            # Passwords are stored in plain JSON for this simple CLI example.
            
            # Replace with secure storage for production use.
            
            # Example default doctor entries:
            
            Doctor("Alice Mwenda", "D101", "docpass"),
            Doctor("Brian Karanja", "D202", "secure123"),
        ]
        save_doctors(doctors)

    doctor = doctor_login_form(doctors)
    run_doctor_cli(doctor)


if __name__ == "__main__":
    main()
