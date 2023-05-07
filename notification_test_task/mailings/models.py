from django.db import models
from django.core.validators import RegexValidator
import pytz
from datetime import datetime

# Create your models here.


class Mailing(models.Model):
    start_date = models.DateTimeField(
        verbose_name="Start DateTIme Mailing"
    )
    end_date = models.DateTimeField(
        verbose_name="End DateTime Mailing"
    )
    mailing_message = models.TextField(
        verbose_name="Mailing Message"
    )
    mobile_phone_code = models.CharField(
        verbose_name="Mobile Phone Code",
        max_length=3,
        blank=True
    )
    client_tag = models.CharField(
        verbose_name="Client Tag",
        max_length=50,
        blank=True
    )

    @property
    def ability_to_send(self) -> bool:
        return self.start_date < datetime.now() < self.end_date

    def __str__(self):
        return f"Mailing {self.id}"


class Client(models.Model):
    phoneNumberRegex = RegexValidator(regex=r"^7\d{10}$")
    phone_number = models.CharField(
        verbose_name="Phone Number",
        validators=[phoneNumberRegex],
        max_length=12,
        unique=True,
        blank=True
    )
    phone_code = models.CharField(
        verbose_name="Phone Number Code",
        max_length=3,
        blank=True
    )
    tag = models.CharField(
        verbose_name="Client Tag",
        max_length=50
    )
    TIMEZONE_CHOICES = zip(pytz.all_timezones, pytz.all_timezones)
    timezone = models.CharField(
        verbose_name="Time Zone",
        max_length=255,
        default='UTC',
        choices=TIMEZONE_CHOICES
    )

    def __str__(self):
        return f"Client: {self.id}. Tag: {self.tag}. Phone number: {self.phone_number}"


class Message(models.Model):
    sending_date = models.DateTimeField(
        verbose_name="DateTime of Sending Message"
    )
    sending_status = models.BooleanField(
        verbose_name="Sending Status",
        default=False
    )
    mailing_id = models.ForeignKey(
        Mailing,
        blank=True,
        on_delete=models.CASCADE
    )
    client_id = models.ForeignKey(
        Client,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"The message {self.id} was sent to the {self.client_id} during the {self.mailing_id}"
