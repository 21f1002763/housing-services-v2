from celery import Celery
from celery.schedules import crontab

def make_celery():
    celery = Celery(
        "housing_services",
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/0",
        include=["tasks"]  # Auto-discover tasks inside `tasks.py`
    )
    return celery

celery = make_celery()  # Celery instance created

# Add the periodic email task
celery.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'tasks.daily_reminder_job',
        'schedule': 10.0,  # Runs every day at 6 PM
    },
    'send-monthly-report': {
        'task': 'tasks.monthly_activity_report',
        'schedule': 10,  # Runs on the 1st of every month at 9 AM
    },

}

celery.conf.timezone = 'UTC'  # Set timezone