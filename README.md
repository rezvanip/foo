# Job Applicant (Beta)

A simple job applicant application (Assignment of University Kivy course)

# Setup

1. Create virtual environment:

```bash
python3 -m venv .venv
```

2. Source the script:

  - Windows:
```console
. .venv/bin/activate.ps1
```
  - Linux:
```console
. .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Initialize database:

```bash
cd src
python3 database/init_db.py
python3 seed_data.py
```

5. Run application:

```bash
python3 main.py
```

Demo credentials: `demo` (username and password)


# TODOs

- [x] Designing the database diagram, app architecture (Repository pattern), creating tables, application skeleton, etc.
- [x] Application UI/UX
   - [x] Register/Login
   - [x] Offers screen
   - [x] Applications screen
   - [x] Profile screen

- [x] How to get file from user?
- [x] Documents
