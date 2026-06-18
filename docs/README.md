# MediTrack Production Flask App

MediTrack is a production-style hospital asset management system built with Flask, SQLAlchemy, Jinja templates, MySQL-ready configuration, and AWS deployment scaffolding.

## Included modules
- Equipment inventory, categories, manufacturers, departments, locations, transfers
- Work orders, preventive maintenance, maintenance records, calibration support
- Vendors, spare parts inventory, procurement basics
- Compliance center, document tracking, audit logging, RBAC
- Dashboard, reports, overdue-maintenance JSON API

## Local setup
1. Create a virtual environment.
2. Install `requirements.txt`.
3. Copy `.env.example` to `.env` and update values.
4. Run `python run.py`.
5. Login with `admin@meditrack.local / Admin@123`.

## AWS deployment outline
1. Provision MySQL RDS and an Ubuntu EC2 instance.
2. Clone this repository on EC2.
3. Create `venv`, install dependencies, and configure `.env`.
4. Test with `gunicorn --bind 127.0.0.1:8000 wsgi:app`.
5. Install `deployment/gunicorn.service` in `/etc/systemd/system/`.
6. Install `deployment/nginx.conf` in `/etc/nginx/sites-available/meditrack`.
7. Reload systemd and Nginx.

## Notes
- The app defaults to SQLite for quick local testing, but `DATABASE_URL` is configured for MySQL on RDS.
- Tables are created automatically at startup for starter use; for stricter production rollout, use Flask-Migrate migrations.
