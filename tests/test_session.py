from session import Session


def test_session_persistence_and_status(tmp_path):
    Session.STORAGE_FILE = tmp_path / "session.json"

    session = Session(patient_id="P001", doctor_id="D101", diagnosis="Test diagnosis")
    stored_sessions = Session.load_all_sessions()

    assert len(stored_sessions) == 1
    assert stored_sessions[0]["patient_id"] == "P001"
    assert stored_sessions[0]["doctor_id"] == "D101"
    assert stored_sessions[0]["diagnosis"] == "Test diagnosis"

    start = session.start_time()
    assert start is not None
    assert session.status == "in-progress"

    end = session.end_time()
    assert end is not None
    assert session.status == "completed"
