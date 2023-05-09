from django.test import TestCase
from django.utils import timezone
from .models import Mailing, Client, Message
from datetime import timedelta


class MailingModelTestCase(TestCase):
    def setUp(self):
        self.mailing = Mailing.objects.create(
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            mailing_message="Hello, world!",
            mobile_phone_code="123",
            client_tag="Tag"
        )

    def test_ability_to_send(self):
        self.assertTrue(self.mailing.ability_to_send)
        self.mailing.start_date = timezone.now() + timedelta(days=1)
        self.mailing.end_date = timezone.now() + timedelta(days=2)
        self.assertFalse(self.mailing.ability_to_send)


class ClientModelTestCase(TestCase):
    def setUp(self):
        self.client = Client.objects.create(
            phone_number="79001234567",
            phone_code="123",
            tag="Tag",
            timezone="UTC"
        )

    def test_phone_number_regex(self):
        invalid_phone_numbers = [
            "88005553535",
            "7911222333a",
            "7911222333444",
            "12345678901",
            "0123456789",
        ]
        for phone_number in invalid_phone_numbers:
            with self.assertRaises(Exception):
                self.client.phone_number = phone_number
                self.client.full_clean()

        valid_phone_numbers = [
            "79001234567",
            "79991234567",
            "79871234567",
        ]
        for phone_number in valid_phone_numbers:
            self.client.phone_number = phone_number
            self.client.full_clean()

    def test_save(self):
        self.client.tag = "New Tag"
        self.client.save()
        self.assertEqual(Client.objects.get(pk=self.client.pk).tag, "New Tag")


class MessageModelTestCase(TestCase):
    def setUp(self):
        self.mailing = Mailing.objects.create(
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            mailing_message="Hello, world!",
            mobile_phone_code="123",
            client_tag="Tag"
        )
        self.client = Client.objects.create(
            phone_number="79001234567",
            phone_code="123",
            tag="Tag",
            timezone="UTC"
        )
        self.message = Message.objects.create(
            mailing=self.mailing,
            client=self.client
        )

    def test_string_representation(self):
        self.assertEqual(
            str(self.message),
            f"The message {self.message.id} was sent to the {self.client.id} during the {self.mailing.id}"
        )
