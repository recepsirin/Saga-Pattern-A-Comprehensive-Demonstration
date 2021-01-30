from saga_transaction_logger import write_transaction
from publisher import publisher
import json
import pika
import yaml

config = dict()

with open("config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('rabbitmq',
                                       5672,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='sec')


def callback(ch, method, properties, body):
    sec_result = json.loads(body)

    if sec_result['sec_channel'] == "booking":

        if sec_result['booking'] == "APPROVED":

            del sec_result['booking']
            write_transaction({"Transaction": "BOOKING IS AVAILABLE",
                               "Booking ID": sec_result['booking_id']})
            publisher(queue="payment", message=sec_result)

        elif sec_result['booking'] == "REJECTED":

            write_transaction({"Transaction": "BOOKING IS NOT AVAILABLE",
                               "Booking ID": sec_result['booking_id']})
            # compensating transaction

    elif sec_result['sec_channel'] == "payment":
        if sec_result['payment'] == "APPROVED":

            write_transaction({"Transaction": "PAYMENT APPROVED - ALL SUCCESSFUL",
                               "Booking ID": sec_result['booking_id'],
                               "Customer ID": sec_result['customer_id']})

        elif sec_result['payment'] == "REJECTED":

            write_transaction({"Transaction": "PAYMENT REJECTED",
                               "Booking ID": sec_result['booking_id']})

            # start compensating for reverting payment
            publisher(queue="flight", message={"booking_id": sec_result['booking_id'],
                                               "booking_date": sec_result['booking_date'],
                                               "transaction": "compensating"})

    elif sec_result['sec_channel'] == "compensating":
        write_transaction({"Transaction": "BOOKING REVERTED BECAUSE CUSTOMER'S BUDGET IS NOT ENOUGH",
                           "Booking ID": sec_result['booking_id']})


channel.basic_consume(queue="sec", on_message_callback=callback, auto_ack=True)

channel.start_consuming()
