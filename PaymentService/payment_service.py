import json
import pika
from pymongo import MongoClient
import yaml
from publisher import publisher

config = dict()

with open("config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='payment')


def callback(ch, method, properties, body):
    payload = json.loads(body)
    with MongoClient(config['mongodb']['dsn']) as client:
        db = client['payment']
        collection = db['payment']
        result = collection.find({"customer_id": payload.get("customer_id"), "wallet": "OK"})

        if result.count() > 0:  # which means customer is able to pay
            publisher(queue="sec", message={
                "sec_channel": "payment",
                "payment": "APPROVED",
                "booking_date": payload['booking_date'],
                "booking_id": payload['booking_id'],
                "customer_id": payload['customer_id'],
                "booking_type": payload['booking_type']
            })
        else:
            # start compensating transactions

            publisher(queue="sec", message={
                "sec_channel": "payment",
                "payment": "REJECTED",
                "booking_date": payload['booking_date'],
                "booking_id": payload['booking_id'],
                "customer_id": payload['customer_id'],
                "booking_type": payload['booking_type']
            })


channel.basic_consume(queue="payment", on_message_callback=callback, auto_ack=True)

channel.start_consuming()
