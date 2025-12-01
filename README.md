# SustiAI — packaged

This repository contains a small demo package for generating carbon accounting reports using a sample SQLite dataset and a small FastAPI wrapper.

Quick commands

Install deps (recommended in a virtualenv):

```bash
python -m pip install -r requirements.txt
```

Create the demo database (ddl + mock data):

```bash
python scripts/create_db.py
```

Run the API locally:

```bash
python main.py
# then visit http://localhost:8000/health
```
