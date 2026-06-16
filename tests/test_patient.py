import json

from patient import Patient


def test_patient_add_and_fetch(tmp_path):
    Patient.FILE_PATH = tmp_path / "patients_data.json"

    patient = Patient(
        name="Test Patient",
        patient_id="P100",
        date_of_birth="2000-01-01",
        phone_number="1234567890",
        height=170,
        weight=70,
    )

    assert patient.add_new_patient() is True

    fetched = Patient.fetch_patient_history("P100")
    assert fetched is not None
    assert fetched["name"] == "Test Patient"
    assert fetched["patient_id"] == "P100"
    assert fetched["phone_number"] == "1234567890"
    assert fetched["height"] == 170
    assert fetched["weight"] == 70

    assert patient.add_new_patient() is False
