import pika
import sys
from faker import Faker
from models import Contacts
from mongoengine import connect


def main(num):
    data = generate_fake_data(num)
    ids = fill_db(data)
    send_data(ids)


def generate_fake_data(num):
    contacts = []
    for _ in range(num):
        contacts.append(
            {"name": Faker().name(),
             "email": Faker().email()}
            )
    return contacts


def fill_db(contacts):

    connect(
        db="testdb",
        host="mongodb://localhost:27017/testdb",
    )
    
    all_id = []

    for item in contacts:
        contact = Contacts(
            name=item.get("name"),
            email=item.get("email")
            )
        contact.save()

        all_id.append(contact.id)

    return all_id


def send_data(ids):

    credentials = pika.PlainCredentials("guest", "guest")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )

    channel = connection.channel()

    channel.queue_declare(queue='contacts_queue')

    for id in ids:
        channel.basic_publish(
            exchange="", routing_key="contacts_queue", body=str(id).encode()
        )

        print(f" [x] Sent {id}")

    connection.close()


if __name__ == "__main__":
    
    try:
        main(5)
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
