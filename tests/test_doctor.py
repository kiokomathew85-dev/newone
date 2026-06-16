from doctor import Doctor, authenticate_doctor, load_doctors, save_doctors


def test_doctor_save_load_and_authenticate(tmp_path):
    Doctor.DOCTORS_FILE = tmp_path / "doctors.json"

    doctor = Doctor("Alice", "D101", "secret123")
    save_doctors([doctor])

    loaded_doctors = load_doctors()
    assert len(loaded_doctors) == 1

    loaded = loaded_doctors[0]
    assert loaded.name == "Alice"
    assert loaded.doctor_id == "D101"
    assert loaded.check_password("secret123") is True
    assert loaded.check_password("wrongpass") is False
    assert "$" in loaded._password

    authenticated = authenticate_doctor(loaded_doctors, "D101", "secret123")
    assert authenticated is not None
    assert authenticated.doctor_id == "D101"
