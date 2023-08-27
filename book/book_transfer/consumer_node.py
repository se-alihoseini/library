import ast
from library import settings

host = settings.RABBITMQ_CONFIG['host']
port = settings.RABBITMQ_CONFIG['port']
username = settings.RABBITMQ_CONFIG['username']
password = settings.RABBITMQ_CONFIG['password']
queue_name = settings.RABBITMQ_CONFIG['queue_name']


def callback_mongo_create(channel, method, properties, body):

    data = body.decode()

    data_dict = ast.literal_eval(data)

    mongo_db = settings.MONGO_DB['mongo_db']
    collection = mongo_db['book']
    collection.insert_one(data_dict)

    channel.basic_ack(delivery_tag=method.delivery_tag)
    channel.stop_consuming()


def callback_mongo_update(channel, method, properties, body):
    data = body.decode()
    data_dict = ast.literal_eval(data)
    mongo_db = settings.MONGO_DB['mongo_db']
    collection = mongo_db['book']

    collection.update_one({'id': data_dict['id']}, {'$set': data_dict})

    channel.basic_ack(delivery_tag=method.delivery_tag)
    channel.stop_consuming()


def co_create_object_mongo(callback):
    connection = settings.RABBITMQ_CONNECTION
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_qos(prefetch_count=1)
    callback_method = eval(callback)
    channel.basic_consume(queue=queue_name, on_message_callback=callback_method)
    channel.start_consuming()
