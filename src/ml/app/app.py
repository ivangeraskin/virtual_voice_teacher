import json
import pika
import sys
import os

from settings import RABBIT_URL, RABBIT_PORT
from process_audio import process

def callback(ch, method, properties, body, args):
    params = json.loads(body)
    print(params)
    result = process(params["file_name"])


def send_task():
    pass


def main():
    input_queue = "voice"
    conn_params = pika.ConnectionParameters(host=RABBIT_URL, port=RABBIT_PORT)
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()
    channel.queue_declare(queue=input_queue)
    channel.basic_consume(queue=input_queue, on_message_callback=callback, auto_ack=True, arguments={"ty": 5})

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()
