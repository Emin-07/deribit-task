import asyncio

from celery import Celery
from celery.schedules import crontab

from core.setup import settings
from services.price_services import create_price_service

celery_app = Celery("worker", broker=settings.REDIS_URL, backend=settings.REDIS_URL)


@celery_app.task
def fetch_deribit_data():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_price_service("eth"))
    loop.run_until_complete(create_price_service("btc"))

    print("Fetching data from Deribit...")
    return "Data saved"


celery_app.conf.beat_schedule = {
    "fetch-every-minute": {
        "task": "celery_app.fetch_deribit_data",
        "schedule": crontab(minute="*"),
    },
}

celery_app.conf.timezone = "UTC"
