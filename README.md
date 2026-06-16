Doctor Portal CLI
==================

A simple CLI for managing doctors, patients, and sessions.

Quick Start
-----------

1. Create a virtual environment (recommended):

```bash
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
# Bash
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run tests:

```bash
python -m pytest
```

4. Start the CLI:

```bash
python main.py
```

Notes
-----
- Data files are stored under the `data/` folder and are created automatically.
- Doctor passwords are hashed when registered. If you previously had plain-text JSON files in the repository root, they were removed to avoid authentication mismatch.
- When running in non-interactive terminals that don't support hidden input, the password prompt will fall back to visible input.

Project Structure
-----------------
- `main.py` — app entrypoint
- `doctor.py` — doctor model and CLI flow
- `patient.py` — patient model and persistence
- `session.py` — session model and persistence
- `storage.py` — knowledge base and diagnosis persistence
- `diagnosis.py` — helper diagnosis flow
- `data/` — JSON storage files
- `tests/` — pytest test cases

Contributing
------------
Use feature branches and open PRs; follow the GitHub flow.

License
-------
MIT-style (add license file if needed)
