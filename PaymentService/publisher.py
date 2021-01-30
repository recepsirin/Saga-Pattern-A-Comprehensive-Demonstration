import pika
import json


def publisher(queue: str, message):
    with pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq')) as connection:
        channel = connection.channel()

        channel.queue_declare(queue=queue)
        channel.basic_publish(exchange='',
                              routing_key=queue,
                              body=json.dumps(message))

        connection.close()
