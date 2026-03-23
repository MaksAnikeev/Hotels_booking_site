from celery import Celery

from src.config import settings


celery_instance = Celery(
    main="tasks", broker=settings.RADIS_URL, include=["src.tasks.tasks"]
)


celery_instance.conf.beat_schedule = {
    "booking_today": {"task": "booking_chek_in_today", "schedule": 11000}
}
