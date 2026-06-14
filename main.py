from session import Session


def main():
   

    # ── Create sessions ──────────────────────────────
    print("\n--- Creating Sessions ---")
    # Option A: uses default 'session.json'
    s1 = Session(patient_id="P001", doctor_id="D101", diagnosis="Hypertension")

    # Option B: point to a custom file path
    # s1 = Session(patient_id="P001", doctor_id="D101", diagnosis="Hypertension", storage_file="data/session.json")

    s2 = Session(patient_id="P002", doctor_id="D101", diagnosis="Diabetes")
    s3 = Session(patient_id="P001", doctor_id="D202", diagnosis="Flu")

    # ── Start session s1 ─────────────────────────────
    print("\n--- Starting Session s1 ---")
    s1.start_time()

    # ── Record notes on s1 ───────────────────────────
    print("\n--- Recording Notes on s1 ---")
    s1.record_notes("Patient reports mild chest pain.")
    s1.record_notes("Blood pressure: 140/90. Prescribed medication.")

    # ── End session s1 ───────────────────────────────
    print("\n--- Ending Session s1 ---")
    s1.end_time()

    # ── Cancel session s2 ────────────────────────────
    print("\n--- Cancelling Session s2 ---")
    s2.update_status("cancelled")

    # ── Search sessions ──────────────────────────────
    print("\n--- Search by doctor_id=D101 ---")
    results = Session.search_session(doctor_id="D101")
    for r in results:
        print(f"  > {r['session_id']} | patient: {r['patient_id']} | status: {r['status']}")

    print("\n--- Search by patient_id=P001 ---")
    results = Session.search_session(patient_id="P001")
    for r in results:
        print(f"  > {r['session_id']} | doctor: {r['doctor_id']} | diagnosis: {r['diagnosis']}")

    # ── Display all sessions ─────────────────────────
    print("\n--- All Sessions in Storage ---")
    for s in Session.load_all_sessions():
        print(
            f"  [{s['status'].upper():12}] "
            f"Session {s['session_id'][:8]}... | "
            f"Patient: {s['patient_id']} | "
            f"Doctor: {s['doctor_id']} | "
            f"Diagnosis: {s['diagnosis']}"
        )

    print("\n" + "=" * 50)
    print("  Done. Data saved to sessions.json")
    print("=" * 50)


if __name__ == "__main__":
    main()