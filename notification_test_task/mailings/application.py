import logging

from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Mailing, Client, Message
from datetime import datetime
from .tasks import send_message
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logger
logging.basicConfig(level=logging.INFO, filename="py_log.txt", filemode="w")


@receiver(post_save, sender=Mailing)
def process_mailing(sender, instance, **kwargs):
    scheduler = BackgroundScheduler()

    if instance.start_time <= datetime.now() < instance.end_time:
        scheduler.add_job(
            send_message,
            trigger=CronTrigger(datetime.now()),
            id="my_job",
            args=[instance.id],
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
    elif instance.start_time > datetime.now():
        scheduler.add_job(
            send_message,
            trigger=CronTrigger(instance.start_time),
            id="my_job",
            args=[instance.id],
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")