import smtplib
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.core.mail import send_mail

from mailing.models import Client, Message, Newsletter, Logs


def send_email():
    """
    Отправляет электронные письма всем клиентам в соответствии с запланированными рассылками.

    Функция проверяет статус каждой рассылки и отправляет письма всем клиентам,
    ведет логирование каждой попытки отправки и обновляет статус рассылок в зависимости от времени.
    """
    # Получение всех клиентов и их email
    clients = Client.objects.all()
    clients_email = []
    for client in clients:
        clients_email.append(getattr(client, 'email'))

    # Получение всех сообщений и их содержимого
    messages = Message.objects.all()
    message_subject = []
    message_body = []
    for message in messages:
        message_subject.append(getattr(message, 'subject'))
        message_body.append(getattr(message, 'body'))

    # Получение текущего времени с учетом часового пояса
    newsletters = Newsletter.objects.all()
    naive_datetime = datetime.now()
    now = naive_datetime.replace(tzinfo=pytz.utc)

    for newsletter in newsletters:
        if newsletter.start_time < now < newsletter.end_time:
            for i in range(len(message_subject)):
                newsletter.status = 'запущена'
                try:
                    # Отправка письма
                    send_mail(
                        subject=message_subject[i],
                        message=message_body[i],
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=clients_email,
                        fail_silently=False,
                    )
                    attempt = True
                    response = 'Рассылка успешно отправлена'
                except smtplib.SMTPException as e:
                    attempt = False
                    response = f'Ошибка при отправке письма: {str(e)}'
                finally:
                    # Логирование попытки отправки для каждого клиента
                    for client in newsletter.client.all():
                        (Logs.objects.create(
                            attempt=attempt, attempt_time=now, response=response, newsletter=newsletter, client=client
                        )).save()

                # Обновление времени начала следующей рассылки в зависимости от периодичности
                if newsletter.periodicity == 'Ежедневно':
                    newsletter.start_time += timedelta(days=1, hours=0, minutes=0)
                elif newsletter.periodicity == 'Еженедельно':
                    newsletter.start_time += timedelta(days=7, hours=0, minutes=0)
                elif newsletter.periodicity == 'Ежемесячно':
                    newsletter.start_time += timedelta(days=30, hours=0, minutes=0)

        elif now > newsletter.end_time:
            newsletter.status = 'завершена'
        elif now < newsletter.start_time:
            newsletter.status = 'создана'

        newsletter.save()
