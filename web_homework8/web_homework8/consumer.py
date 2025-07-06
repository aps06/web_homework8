import pika
import sys
from mongoengine import connect
from models import Contacts

connect(
    db="testdb",
    host="mongodb://localhost:27017/testdb")


def main():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue="contacts_queue")

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        change_contact(id=body.decode())

    channel.basic_consume(
        queue="contacts_queue", on_message_callback=callback, auto_ack=True
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


def change_contact(id):

    contact = Contacts.objects(id=id).first()
    contact.send_mesage = True
    contact.save()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
