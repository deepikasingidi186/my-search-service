import json
import os
import pika

from src.services.search_index import index_document

print("Worker process booting...", flush=True)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_NAME = "search_indexing_queue"


def callback(ch, method, properties, body):
    print("Received message from queue", flush=True)

    try:
        message = json.loads(body)
        document = message["document"]

        index_document(document)

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("Document indexed and ACK sent", flush=True)

    except Exception as e:
        print("Indexing failed:", str(e), flush=True)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def start_worker():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback
    )

    print("Indexing worker started and waiting for messages...", flush=True)
    channel.start_consuming()


if __name__ == "__main__":
    start_worker()
