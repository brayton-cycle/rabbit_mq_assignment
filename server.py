import pika
import json
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

def callback(ch, method, properties, body):
    message = json.loads(body)
    message['timestamp'] = datetime.now()

    # Inserting messages into MongoDB
    db.mqtt_messages.insert_one(message)
    print(f"Received and saved: {message}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

def mqtt_consumer():
    # Connecting to Mongo DB server on AWS EC2 instance using public IP
    client = MongoClient(os.getenv("MONGO_DB_URI"))
    global db
    db = client.mqtt_database
    print("Connected to MongoDB:", db)
 

    # Connecting to RabbitMQ server on cloud AMQP
    connection = pika.BlockingConnection(pika.URLParameters(os.getenv("RABBIT_MQ_URI")))
    channel = connection.channel()

    # Declare the queue (ensure it exists)
    channel.queue_declare(queue='mqtt_queue', durable=True)

    channel.basic_consume(queue='mqtt_queue', on_message_callback=callback)

    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    mqtt_consumer()
