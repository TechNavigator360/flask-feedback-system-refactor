# KCC Coaching Tool (Refactor Project)

## Context

This project started as a Tkinter-based desktop application built in Jupyter Notebook as part of a learning assignment.

The goal of this refactor is to transform that prototype into a structured, testable, and web-based application using Flask.

---

## Goals of this refactor

- Move from UI-driven logic → service-based architecture
- Separate concerns (UI, business logic, data access)
- Introduce testing (pytest)
- Replace Tkinter with a web interface (Flask + Jinja + CSS)
- Prepare the application for future backend improvements (e.g. database, authentication)

---

## Current stack

- Python
- Flask (web framework)
- Jinja2 (templating)
- HTML / CSS
- CSV (temporary persistence layer)
- Pytest (testing)

---

## Architecture

```text
Browser
  ↓
Flask routes (app.py)
  ↓
Services (business logic)
  ↓
Repositories (CSV persistence)
  ↓
data.csv
```
---

## Structure

```
src/
  services/
    auth_service.py
    user_service.py
    feedback_service.py

  repositories/
    csv_repository.py

templates/
static/css/
tests/
```
---

## Features (current)
- Login (Agent / Coach)
- Agent dashboard (view feedback)
- Coach dashboard
- Create user accounts
- Add feedback
- View feedback

---

## Testing
Business logic is tested using pytest.

Run tests:

```
PYTHONPATH=. python -m pytest
```

---

## Running the application
```
PYTHONPATH=. python app.py
```
Open:
```
http://127.0.0.1:5000
```

---

## Notes
- Passwords are currently stored in plain text (planned improvement)
- CSV is used as a temporary data store (planned migration to database)
- This project is actively being refactored and extended

---

### Latest update

Implemented coach feedback status updates.

Coaches can now change feedback from `Not Integrated` to `Integrated`.  
The update goes through the Flask route, service layer, and CSV repository flow.

Tested with pytest:

- 11 tests passing
- feedback creation tests
- feedback status update tests
- authentication/user service tests