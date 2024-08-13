from django.core.management import BaseCommand
from mailing.models import Mailing, Message, Customers, Mailing_attempt
import json


class Command(BaseCommand):

    @staticmethod
    def json_read_mailing():
        with open('mailing.json', encoding='utf-8') as json_file:
            return json.load(json_file)

    @staticmethod
    def json_read_message():
        with open('message.json', encoding='utf-8') as json_file:
            return json.load(json_file)

    @staticmethod
    def json_read_customers():
        with open('customers.json', encoding='utf-8') as json_file:
            return json.load(json_file)

    @staticmethod
    def json_read_mailing_attempt():
        with open('mailing_attempt', encoding='utf-8') as json_file:
            return json.load(json_file)

    def handle(self, *args, **options):

        # Удалите все рассылки
        Mailing.objects.all().delete()
        # Сброс индефикатора Рассылок
        Mailing.truncate_table_restart_id()
        # Удалите все Сообщения
        Message.objects.all().delete()
        # Удалите все Клентов
        Customers.objects.all().delete()
        # Удалите все Настройки рассылок
        Mailing_attempt.objects.all().delete()

        mailing_list = []
        message_list = []
        customer_list = []
        mailing_at_list = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for mailing in Command.json_read_mailing():
            mailing_list.append(
                {"id": mailing['pk'], "start_time": mailing['fields']['start_time'],
                 "end_time": mailing['fields']['end_time'], "next_day": mailing['fields']['next_day'],
                 "frequency": mailing['fields']['frequency'], "mailing_status": mailing['fields']['mailing_status']}
            )
        mailing_for_create = []
        for mailing_item in mailing_list:
            mailing_for_create.append(
                Mailing.objects.create(**mailing_item)
            )

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for message in Command.json_read_message():
            message_list.append(
                {"id": message['pk'], "mailing": Mailing.objects.get(pk=message['fields']['mailing']),
                 "subject_message": message['fields']['subject_message'],
                 "message": message['fields']['message']}
            )
        message_for_create = []
        for message_item in message_list:
            message_for_create.append(
                Message.objects.create(**message_item)
            )

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for customer in Command.json_read_customers():
            customer_list.append(
                {"id": customer['pk'], "mailing": Mailing.objects.get(pk=message['fields']['mailing']),
                 "email": customer['fields']['email'],
                 "fio": customer['fields']['fio'], "comment": customer['fields']['comment']}
            )
        customer_for_create = []
        for customer_item in customer_list:
            customer_for_create.append(
                Message.objects.create(**customer_item)
            )

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for mailing_attempt in Command.json_read_mailing_attempt():
            mailing_at_list.append(
                {"id": mailing_attempt['pk'], "mailing": Mailing.objects.get(pk=message['fields']['mailing']),
                 "last_attempt": mailing_attempt['fields']['last_attempt'],
                 "status": mailing_attempt['fields']['status'],
                 "mail_response": mailing_attempt['fields']['mail_response']}
            )
        mailing_attempt_for_create = []
        for mailing_attempt_item in mailing_at_list:
            mailing_attempt_for_create.append(
                Message.objects.create(**mailing_attempt_item)
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Mailing.objects.bulk_create(mailing_for_create)
        Message.objects.bulk_create(message_for_create)
        Customers.objects.bulk_create(message_for_create)
        Mailing_attempt.objects.bulk_create(message_for_create)
