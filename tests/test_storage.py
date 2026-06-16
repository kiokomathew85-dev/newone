import json

from storage import StorageEngine


def test_storage_engine_search_and_save(tmp_path):
    kb_path = tmp_path / "knowledge_base.json"
    diagnosis_path = tmp_path / "diagnosis.json"

    knowledge_data = {
        "diseases": [
            {
                "name": "Flu",
                "symptoms": ["fever", "cough"],
                "prevention": "rest",
                "medication": "flu meds",
            }
        ]
    }
    kb_path.write_text(json.dumps(knowledge_data))

    engine = StorageEngine(kb_path=str(kb_path), diagnosis_path=str(diagnosis_path))
    matches = engine.search_diseases_by_symptom("fever")

    assert len(matches) == 1
    assert matches[0]["name"] == "Flu"

    assert engine.save_diagnosis({
        "session_id": "S1",
        "patient_id": "P001",
        "doctor_id": "D101",
        "symptoms": "fever",
        "disease": "Flu",
        "prevention": "rest",
        "medication": "flu meds",
    }) is True

    saved_data = json.loads(diagnosis_path.read_text())
    assert isinstance(saved_data, list)
    assert saved_data[0]["disease"] == "Flu"
