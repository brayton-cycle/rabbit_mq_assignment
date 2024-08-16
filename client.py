import pika
import json
import random
import time
import os
from dotenv import load_dotenv
load_dotenv()

def mqtt_producer():
    # Establish connection to RabbitMQ
    connection = pika.BlockingConnection(pika.URLParameters(os.getenv("MONGO_DB_URI")))
    channel = connection.channel()
    print("connected to channnel", channel)

    # Declare a queue
    channel.queue_declare(queue='mqtt_queue', durable=True)

    while True:
        # Generate a random status
        status = random.randint(0, 6)
        message = {'status': status}

        # Publish the message to the queue
        channel.basic_publish(
            exchange='',
            routing_key='mqtt_queue',
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        
        print(f"Sent: {message}")
        time.sleep(1)  # Emit message every second

if __name__ == "__main__":
    mqtt_producer()
