# Job Applicant

A simple job applicant application (Assignment of University Kivy course)

# Setup

1. Create virtual environment:

```bash
   python3 -m venv .venv
   source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Initialize database:

```bash
   cd src
   python3 database/init_db.py
   python3 seed_data.py
```

4. Run application:

```bash
   python3 main.py
```

Demo credentials: `demo` (username and password)


# TODOs

- [ ] Designing the database diagram, app architecture (Repository pattern), creating tables, application skeleton, etc.
- [ ] Application UI/UX
   - [ ] Register/Login (@)
   - [ ] Offers screen
   - [ ] Applications screen
   - [ ] Profile screen

- [ ] How to get file from user?
- [ ] CI/CD (Exec, APKs artifacts)
- [ ] Documents