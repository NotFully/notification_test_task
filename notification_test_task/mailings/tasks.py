import apscheduler.jobstores.base
import requests
from .models import Mailing, Client, Message
from time import sleep
from django.db.models import Q



TKN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTQ4MjkwOTMsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9uaWxsb3JfciJ9.IUCuehOdksul7FtaN9ETR8NZ-PwtEJ09d8rUqlDX19A"
URL = "https://probe.fbrq.cloud/v1/send/"


def send_message(m_id,  token=TKN, url=URL):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    mailing = Mailing.objects.filter(id=m_id).first()
    clients = Client.objects.filter(
        Q(tag=mailing.client_tag) |
        Q(phone_code=mailing.mobile_phone_code)
    ).all()
    for client in clients:
        # msg = Message(mailing_id=instance.id, client_id=client.id)
        # msg.save()
        Message.objects.create(mailing_id=m_id, client_id=client.id)
        message = Message.objects.filter(mailing_id=m_id).filter(client_id=client.id).first()
        data = {
            "id": message.id,
            "phone": client.phone_number,
            "text": mailing.mailing_message
        }

        flag = False
        while not flag:
            try:
                response = requests.post(url=url+str(data["id"]), headers=headers, json=data)
                print(f"Request on {url + str(data['id'])} Status {response.status_code}")
                if response.status_code == 200:
                    flag = True
                    message.sending_status = True
                    message.save()
            except ValueError:
                return f"ValueError retrying"
            except ConnectionError:
                return f"ConnectionError"


