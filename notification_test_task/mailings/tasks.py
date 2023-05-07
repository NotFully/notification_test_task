import requests
from .models import Mailing, Client, Message
from django.db.models import Q


TKN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTQ4MjkwOTMsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9uaWxsb3JfciJ9.IUCuehOdksul7FtaN9ETR8NZ-PwtEJ09d8rUqlDX19A"
URL = "https://probe.fbrq.cloud/v1/send/"


def send_message(mailing_id, token=TKN, url=URL):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    mailing = Mailing.objects.filter(id=mailing_id).first()
    clients = Client.objects.filter(
        Q(mailing.client_tag) |
        Q(mailing.mobile_phone_code)
    ).all()

    for client in clients:
        messages = Message.objects.filter(mailing_id=mailing.id).filter(client_id=client.id).all()
        for message in messages:
            data = {
                {
                    "id": mailing.id,
                    "phone": client.phone_number,
                    "text": mailing.mailing_message
                }
            }
            try:
                response = requests.post(url=url+str(message.id), headers=headers, json=data)
                print(response)
            except ConnectionError:
                return f"ConnectionError"


