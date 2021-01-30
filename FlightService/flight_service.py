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

channel.queue_declare(queue='flight')


def callback(ch, method, properties, body):
    with MongoClient('mongodb://flight_db:27018/') as client:
        db = client['flights']
        collection = db['flights']
        consumed_data = json.loads(body)
        result = collection.find({"available": True, "date": consumed_data["booking_date"]})
        # check there are any compensating transaction demand
        if consumed_data['transaction'] == "compensating":

            collection.update_one(
                {"available": False,
                 "date": consumed_data["booking_date"],
                 "reserved": consumed_data["booking_id"]},

                {"$set":
                     {"available": True,
                      "date": consumed_data["booking_date"]}})

            publisher(queue="sec", message={
                "sec_channel": "compensating",
                "compensating": True,
                "type": "booking",
                "booking_date": consumed_data['booking_date'],
                "booking_id": consumed_data['booking_id']
            })

        elif consumed_data['transaction'] == "commit":
            if result.count() > 0:  # which means there are available requested flights

                collection.update_one({"available": True, "date": consumed_data["booking_date"]},
                                      {"$set":
                                           {"available": False, "date": consumed_data["booking_date"],
                                            "reserved": consumed_data["booking_id"]}})
                # being given info to start payment transactions
                publisher(queue="sec", message={
                    "sec_channel": "booking",
                    "booking": "APPROVED",
                    "booking_date": consumed_data['booking_date'],
                    "booking_id": consumed_data['booking_id'],
                    "customer_id": consumed_data['customer_id'],
                    "booking_type": consumed_data['booking_type']
                })

            else:
                # start compensating transactions
                publisher(queue="sec", message={
                    "sec_channel": "booking",
                    "booking": "REJECTED",
                    "booking_date": consumed_data['booking_date'],
                    "booking_id": consumed_data['booking_id'],
                    "customer_id": consumed_data['customer_id'],
                    "booking_type": consumed_data['booking_type']
                })


channel.basic_consume(queue="flight", on_message_callback=callback, auto_ack=True)

channel.start_consuming()
