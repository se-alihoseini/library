import pika
from library import settings

host = settings.RABBITMQ_CONFIG['host']
port = settings.RABBITMQ_CONFIG['port']
username = settings.RABBITMQ_CONFIG['username']
password = settings.RABBITMQ_CONFIG['password']
queue_name = settings.RABBITMQ_CONFIG['queue_name']


def pr_create_object_mongo(message):

    connection = settings.RABBITMQ_CONNECTION
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(exchange='', routing_key=queue_name, body=message,
                          properties=pika.BasicProperties(delivery_mode=2))
    channel.close()
