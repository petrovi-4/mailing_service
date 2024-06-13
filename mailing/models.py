from django.conf import settings
from django.db import models

from config.settings import NULLABLE


class Client(models.Model):
    email = models.EmailField(verbose_name='почта', unique=True)
    fio = models.CharField(max_length=50, verbose_name='ФИО')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return f'ФИО: {self.fio}, почта: {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    subject = models.CharField(max_length=30, verbose_name='Тема письма')
    body = models.TextField(verbose_name='тело письма')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return {self.subject}

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Newsletter(models.Model):
    start_time = models.DateTimeField(verbose_name='время начала отправки рассылки')
    end_time = models.DateTimeField(verbose_name='время окончания отправки рассылки')

    period_choices = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]
    periodicity = models.CharField(
        max_length=10,
        choices=period_choices,
        verbose_name='периодичность рассылки',
    )
    status_choices = [
        ('created', 'Created'),
        ('started', 'Started'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(
        max_length=10,
        choices=status_choices,
        verbose_name='статус рассылки',
    )
    client = models.ManyToManyField(Client, verbose_name='клиент', blank=True)
    message = models.ForeignKey(Message, verbose_name='сообщение',  on_delete=models.CASCADE, **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return f'Время: {self.start_time} - {self.end_time}, статус рассылки: {self.status}, периодичность рассылки: {self.periodicity}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

        permissions = [
            ('change_status', 'Can change newsletter status'),
        ]


class Logs(models.Model):
    attempt = models.BooleanField(verbose_name='статус попытки')
    attempt_time = models.DateTimeField(verbose_name='дата и время последней попытки')
    response = models.CharField(max_length=100, verbose_name='ответ почтового сервера', **NULLABLE)

    newsletter = models.ForeignKey(Newsletter, verbose_name='рассылка', null=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(Client, verbose_name='клиент', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return (f'Статус попытки: {self.attempt}, дата и время последней попытки: {self.attempt_time}, ответ почтового сервера:'
                f' {self.response}')

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'


class Contact(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    number = models.TextField(verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Email')

    def __str__(self):
        return f'{self.name} {self.number}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
