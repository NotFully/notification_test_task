from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Mailing, Client, Message
from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import send_message
from django.utils import timezone
from apscheduler.triggers.cron import CronTrigger


@receiver(post_save, sender=Mailing)
def process_mailing(sender, instance, created, **kwargs):
    if created:
        scheduler = BackgroundScheduler()
        scheduler.start()
        if instance.ability_to_send:
            scheduler.add_job(
                send_message,
                run_date=timezone.now(),
                args=[instance.id],
                id=f"my_job"
            )
        else:
            scheduler.add_job(
                send_message,
                run_date=instance.start_date,
                args=[instance.id],
                id=f"my_job"
            )


